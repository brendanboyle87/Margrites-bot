from margrites.rules import apply_step
from margrites.state import GameState
from margrites.types import alg_to_coord


def test_capture_chain_removes_multiple_enemies():
    black_positions = [
        alg_to_coord("d5"),
        alg_to_coord("e5"),
        alg_to_coord("f5"),
        alg_to_coord("f6"),
    ]
    white_positions = [alg_to_coord("e6"), alg_to_coord("e7")]
    state = GameState.from_setup(black=black_positions, white=white_positions)
    move_src = alg_to_coord("d5")
    move_dst = alg_to_coord("d6")
    e6 = alg_to_coord("e6")
    e7 = alg_to_coord("e7")
    new_state = apply_step(state, (move_src, move_dst))
    assert new_state.board[e6[0]][e6[1]] == 0
    assert new_state.board[e7[0]][e7[1]] == 0
    assert new_state.captures[+1] == 2
    assert new_state.board[move_dst[0]][move_dst[1]] == +1
