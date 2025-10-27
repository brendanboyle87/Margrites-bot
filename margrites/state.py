"""Game state representation for Margrites."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .types import (
    BOARD_COLS,
    BOARD_ROWS,
    MAX_MOVES_PER_TURN,
    Coord,
    Player,
)


@dataclass
class GameState:
    board: List[List[int]]
    to_move: Player
    moves_left: int
    start_squares: Dict[Coord, Coord] = field(default_factory=dict)
    score: Dict[Player, int] = field(default_factory=lambda: {+1: 0, -1: 0})
    captures: Dict[Player, int] = field(default_factory=lambda: {+1: 0, -1: 0})

    def clone(self) -> "GameState":
        return GameState(
            board=[row[:] for row in self.board],
            to_move=self.to_move,
            moves_left=self.moves_left,
            start_squares=dict(self.start_squares),
            score=dict(self.score),
            captures=dict(self.captures),
        )

    def serialize(self) -> dict:
        return {
            "board": [row[:] for row in self.board],
            "to_move": self.to_move,
            "moves_left": self.moves_left,
            "start_squares": {k: v for k, v in self.start_squares.items()},
            "score": dict(self.score),
            "captures": dict(self.captures),
        }

    @staticmethod
    def from_setup(
        black: List[Coord],
        white: List[Coord],
        to_move: Player = +1,
    ) -> "GameState":
        board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        for coord in black:
            r, c = coord
            _ensure_on_board(coord)
            if board[r][c] != 0:
                raise ValueError(f"Duplicate placement at {coord}")
            board[r][c] = +1
        for coord in white:
            r, c = coord
            _ensure_on_board(coord)
            if board[r][c] != 0:
                raise ValueError(f"Duplicate placement at {coord}")
            board[r][c] = -1
        return GameState(
            board=board,
            to_move=to_move,
            moves_left=MAX_MOVES_PER_TURN,
        )

    def piece_count(self) -> Dict[Player, int]:
        counts = {+1: 0, -1: 0}
        for row in self.board:
            for value in row:
                if value == +1:
                    counts[+1] += 1
                elif value == -1:
                    counts[-1] += 1
        return counts


def _ensure_on_board(coord: Coord) -> None:
    r, c = coord
    if not (0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS):
        raise ValueError(f"Coordinate {coord} is out of bounds")
