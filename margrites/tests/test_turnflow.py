from margrites.rules import apply_step, legal_steps
from margrites.state import GameState
from margrites.types import alg_to_coord, scoring_notation


def test_scoring_consumes_move_and_removes_piece():
    src = alg_to_coord("e8")
    state = GameState.from_setup(black=[src], white=[])
    step = (src, scoring_notation(+1))
    assert step in legal_steps(state)
    new_state = apply_step(state, step)
    assert new_state.board[src[0]][src[1]] == 0
    assert new_state.score[+1] == 1
    assert new_state.to_move == -1
    assert new_state.moves_left == 4


def test_trapping_forfeits_remaining_moves():
    src = alg_to_coord("b2")
    trap_move = (src, alg_to_coord("a1"))
    state = GameState.from_setup(
        black=[src],
        white=[alg_to_coord("a2"), alg_to_coord("c1"), alg_to_coord("c2")],
    )
    assert trap_move in legal_steps(state)
    new_state = apply_step(state, trap_move)
    assert new_state.to_move == -1
    assert new_state.moves_left == 4
