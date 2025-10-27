from margrites.engine import play_turn
from margrites.state import GameState
from margrites.types import alg_to_coord, scoring_notation


def test_scoring_sequence_four_steps():
    e5 = alg_to_coord("e5")
    e6 = alg_to_coord("e6")
    e7 = alg_to_coord("e7")
    e8 = alg_to_coord("e8")
    state = GameState.from_setup(black=[e5], white=[])
    sequence = [(e5, e6), (e6, e7), (e7, e8), (e8, scoring_notation(+1))]
    final_state = play_turn(state, sequence)
    assert final_state.score[+1] == 1
    assert all(final_state.board[row][col] == 0 for row in range(len(final_state.board)) for col in range(len(final_state.board[0])))
    assert final_state.to_move == -1
    assert final_state.moves_left == 4


def test_scoring_in_one_move():
    e8 = alg_to_coord("e8")
    state = GameState.from_setup(black=[e8], white=[])
    final_state = play_turn(state, [(e8, scoring_notation(+1))])
    assert final_state.score[+1] == 1
    assert final_state.to_move == -1
    assert final_state.moves_left == 4
