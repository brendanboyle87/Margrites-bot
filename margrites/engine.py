"""High-level turn handling for Margrites."""
from __future__ import annotations

from typing import Sequence

from .rules import apply_step, legal_steps
from .state import GameState
from .types import MAX_MOVES_PER_TURN


def play_turn(state: GameState, step_sequence: Sequence) -> GameState:
    """Apply a sequence of up to four legal steps for the current player."""
    if state.moves_left != MAX_MOVES_PER_TURN:
        raise ValueError("play_turn must be called at the start of a turn")

    working_state = state
    for index, step in enumerate(step_sequence):
        legal = legal_steps(working_state)
        if step not in legal:
            raise ValueError(f"Illegal step {step} at position {index}")
        working_state = apply_step(working_state, step)
        if working_state.moves_left == MAX_MOVES_PER_TURN:
            # Turn ended prematurely (trap or exhausted moves)
            if index + 1 < len(step_sequence):
                raise ValueError("Turn ended before all steps were used")
            break
    return working_state


def legal_turn_exists(state: GameState) -> bool:
    return bool(legal_steps(state))
