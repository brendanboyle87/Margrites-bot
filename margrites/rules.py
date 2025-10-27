"""Core rules engine for Margrites."""
from __future__ import annotations

from typing import Dict, List, Tuple

from .state import GameState
from .types import (
    BOARD_COLS,
    BOARD_ROWS,
    MAX_MOVES_PER_TURN,
    Coord,
    Player,
    neighbors,
    scoring_notation,
)

Step = Tuple[Coord, Coord] | Tuple[Coord, str]


def legal_steps(state: GameState) -> List[Step]:
    if state.moves_left <= 0:
        return []

    board = state.board
    player = state.to_move
    steps: List[Step] = []

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] != player:
                continue
            src = (r, c)
            _collect_piece_steps(state, src, steps)

    return steps


def _collect_piece_steps(state: GameState, src: Coord, steps: List[Step]) -> None:
    player = state.to_move
    board = state.board
    sr, sc = src
    start_square = state.start_squares.get(src, src)

    # Normal neighbouring moves
    for dst in neighbors(src):
        dr, dc = dst
        if board[dr][dc] != 0:
            continue
        if dst == start_square:
            continue
        if _move_is_martyrdom(state, src, dst):
            continue
        steps.append((src, dst))

    # Scoring move
    if sr == (0 if player == 1 else BOARD_ROWS - 1):
        steps.append((src, scoring_notation(player)))


def _move_is_martyrdom(state: GameState, src: Coord, dst: Coord) -> bool:
    board_copy = [row[:] for row in state.board]
    piece = board_copy[src[0]][src[1]]
    board_copy[src[0]][src[1]] = 0
    board_copy[dst[0]][dst[1]] = piece
    _resolve_captures_on_board(board_copy)
    return board_copy[dst[0]][dst[1]] != piece


def _resolve_captures_on_board(board: List[List[int]]) -> None:
    while True:
        to_capture: List[Tuple[int, int, int]] = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece = board[r][c]
                if piece == 0:
                    continue
                if _is_captured(board, (r, c), piece):
                    to_capture.append((r, c, piece))
        if not to_capture:
            break
        for r, c, _piece in to_capture:
            board[r][c] = 0


def _is_captured(board: List[List[int]], coord: Coord, piece: Player) -> bool:
    opp = 0
    ally = 1
    for nr, nc in neighbors(coord):
        if board[nr][nc] == -piece:
            opp += 1
        elif board[nr][nc] == piece:
            ally += 1
    return opp >= 2 * ally


def apply_step(state: GameState, step: Step) -> GameState:
    legal = legal_steps(state)
    if step not in legal:
        raise ValueError(f"Illegal step {step}")

    new_state = state.clone()
    player = state.to_move
    board = new_state.board
    src = step[0]

    if isinstance(step[1], tuple):
        dst = step[1]
        start_square = new_state.start_squares.pop(src, src)
        piece = board[src[0]][src[1]]
        board[src[0]][src[1]] = 0
        board[dst[0]][dst[1]] = piece
        new_state.start_squares[dst] = start_square
    else:
        # scoring move
        board[src[0]][src[1]] = 0
        new_state.start_squares.pop(src, None)
        new_state.score[player] = new_state.score.get(player, 0) + 1

    resolve_captures(new_state)

    new_state.moves_left -= 1
    if new_state.moves_left <= 0 or not legal_steps(new_state):
        _end_turn(new_state)
    return new_state


def resolve_captures(state: GameState) -> None:
    board = state.board
    changed = True
    while changed:
        changed = False
        to_capture: List[Tuple[int, int, int]] = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece = board[r][c]
                if piece == 0:
                    continue
                if _is_captured(board, (r, c), piece):
                    to_capture.append((r, c, piece))
        if not to_capture:
            continue
        changed = True
        for r, c, piece in to_capture:
            board[r][c] = 0
            state.captures[-piece] = state.captures.get(-piece, 0) + 1
            state.start_squares.pop((r, c), None)


def _end_turn(state: GameState) -> None:
    state.to_move = -state.to_move
    state.moves_left = MAX_MOVES_PER_TURN
    state.start_squares.clear()


def is_terminal(state: GameState) -> bool:
    counts = state.piece_count()
    return counts[+1] == 0 or counts[-1] == 0


def result(state: GameState) -> Dict[str, int | str]:
    points_black = state.score.get(+1, 0)
    points_white = state.score.get(-1, 0)
    captures_black = state.captures.get(+1, 0)
    captures_white = state.captures.get(-1, 0)

    if points_black > points_white:
        winner = "black"
    elif points_white > points_black:
        winner = "white"
    elif captures_black > captures_white:
        winner = "black"
    elif captures_white > captures_black:
        winner = "white"
    else:
        winner = "draw"

    return {
        "points_black": points_black,
        "points_white": points_white,
        "captures_black": captures_black,
        "captures_white": captures_white,
        "winner": winner,
    }
