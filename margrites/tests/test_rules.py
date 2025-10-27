from margrites.rules import apply_step, legal_steps
from margrites.state import GameState
from margrites.types import alg_to_coord


def test_neighbors_allow_diagonals():
    state = GameState.from_setup(black=[alg_to_coord("e5")], white=[])
    steps = legal_steps(state)
    destinations = {step[1] for step in steps if isinstance(step[1], tuple)}
    expected = {
        alg_to_coord(square)
        for square in ["d4", "d5", "d6", "e4", "e6", "f4", "f5", "f6"]
    }
    assert destinations == expected


def test_martyrdom_blocks_suicide_step():
    black_piece = alg_to_coord("e5")
    destination = alg_to_coord("d6")
    enemy_a = alg_to_coord("c6")
    enemy_b = alg_to_coord("d7")
    state = GameState.from_setup(black=[black_piece], white=[enemy_a, enemy_b])
    steps = legal_steps(state)
    assert (black_piece, destination) not in steps


def test_no_return_to_start_square():
    start = alg_to_coord("e5")
    first_step = (start, alg_to_coord("e6"))
    state = GameState.from_setup(black=[start], white=[])
    next_state = apply_step(state, first_step)
    assert (first_step[1], start) not in legal_steps(next_state)
