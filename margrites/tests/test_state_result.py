from margrites.rules import is_terminal, result
from margrites.state import GameState
from margrites.types import alg_to_coord


def test_terminal_and_winner_tie_break_by_captures():
    state = GameState.from_setup(black=[], white=[alg_to_coord("a1")])
    state.score[+1] = 3
    state.score[-1] = 3
    state.captures[+1] = 4
    state.captures[-1] = 2
    assert is_terminal(state)
    outcome = result(state)
    assert outcome["winner"] == "black"
    assert outcome["points_black"] == 3
    assert outcome["points_white"] == 3
    assert outcome["captures_black"] == 4
    assert outcome["captures_white"] == 2
