"""Core types and coordinate helpers for the Margrites simulator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]
Player = int

BOARD_ROWS = 8
BOARD_COLS = 9
MAX_MOVES_PER_TURN = 4

COLUMN_LABELS = "abcdefghi"
RANK_LABELS = "12345678"


def on_board(coord: Coord) -> bool:
    """Return True if *coord* is inside the 9×8 board."""
    r, c = coord
    return 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS


def neighbors(coord: Coord) -> List[Coord]:
    """Return all orthogonal and diagonal neighbours on the board."""
    r, c = coord
    result: List[Coord] = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if on_board((nr, nc)):
                result.append((nr, nc))
    return result


def opponent(player: Player) -> Player:
    return -player


def last_rank(player: Player) -> int:
    return 0 if player == 1 else BOARD_ROWS - 1


def forward_direction(player: Player) -> int:
    # Player +1 advances towards row 0 (upwards); player -1 advances towards row 7 (downwards).
    return -player


def scoring_notation(player: Player) -> str:
    return "B++" if player == 1 else "W++"


def coord_to_alg(coord: Coord) -> str:
    r, c = coord
    if not on_board(coord):
        raise ValueError(f"Coordinate {coord} out of bounds")
    file_char = COLUMN_LABELS[c]
    rank_char = RANK_LABELS[-(r + 1)]  # rows 0..7 correspond to ranks 8..1
    return f"{file_char}{rank_char}"


def alg_to_coord(square: str) -> Coord:
    if len(square) != 2:
        raise ValueError(f"Invalid square notation: {square}")
    file_char, rank_char = square[0], square[1]
    if file_char not in COLUMN_LABELS or rank_char not in RANK_LABELS:
        raise ValueError(f"Invalid square notation: {square}")
    col = COLUMN_LABELS.index(file_char)
    # ranks are 1..8 bottom to top; row 0 is rank 8
    row = len(RANK_LABELS) - RANK_LABELS.index(rank_char) - 1
    return (row, col)


@dataclass
class MoveRecord:
    src: Coord
    dst: Coord | str


__all__ = [
    "Coord",
    "Player",
    "BOARD_ROWS",
    "BOARD_COLS",
    "MAX_MOVES_PER_TURN",
    "on_board",
    "neighbors",
    "opponent",
    "last_rank",
    "forward_direction",
    "scoring_notation",
    "coord_to_alg",
    "alg_to_coord",
    "MoveRecord",
]
