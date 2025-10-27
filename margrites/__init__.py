"""Public API for the Margrites simulator."""
from .engine import legal_turn_exists, play_turn
from .rules import apply_step, is_terminal, legal_steps, resolve_captures, result
from .state import GameState
from .types import (
    BOARD_COLS,
    BOARD_ROWS,
    MAX_MOVES_PER_TURN,
    Coord,
    Player,
    alg_to_coord,
    coord_to_alg,
    neighbors,
    opponent,
    scoring_notation,
)

__all__ = [
    "GameState",
    "legal_steps",
    "apply_step",
    "resolve_captures",
    "is_terminal",
    "result",
    "play_turn",
    "legal_turn_exists",
    "Coord",
    "Player",
    "alg_to_coord",
    "coord_to_alg",
    "neighbors",
    "opponent",
    "scoring_notation",
    "BOARD_ROWS",
    "BOARD_COLS",
    "MAX_MOVES_PER_TURN",
]
