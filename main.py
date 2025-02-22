from at3.parse import parse

from engine.board import Board
from engine.enums import GameState, Mark, Player, Result
from engine.exceptions import MoveScriptBreak
from engine.game import Game
from engine.move import Move


def show_board(g: Game):
    print(f"{g.cur_player=} {g.state=} {g.result}")
    print(g.board.pretty(coords=True))
    print()


def parse_move_script_line(line: str) -> Move:
    if line == "break":
        raise MoveScriptBreak

    coords, mark_str = line.split(" ")

    row, col = map(int, coords.split(","))
    mark = Mark.from_str(mark_str)

    return Move(row, col, mark)


def play_move_script(g: Game, script: str):
    show_board(g)

    for line in script.split('\n'):
        line = line.strip()
        if not line:
            continue

        move = parse_move_script_line(line)

        g.apply_move(move)

        show_board(g)


def assert_game_state(wanted: GameState, got: GameState):
    assert wanted == got, f"{wanted=} {got=}"


def assert_player(wanted: Player, got: Player):
    assert wanted == got, f"{wanted=} as the winner, {got=} instead"


def assert_result(wanted: Result, got: Result):
    assert wanted == got, f"{wanted=} as result, {got=} instead"


def test_player1_row_win():
    b = Board()
    g = Game(b)

    script = """
    1,2 X
    0,2 O
    1,0 X
    2,0 O
    1,1 X
    """

    play_move_script(g, script)

    assert_game_state(GameState.FINISHED, g.state)
    assert_result(Result.PLAYER1_VICTORY, g.result)


def test_player2_col_win():
    b = Board()
    g = Game(b)

    script = """
    1,1 X
    0,2 O
    1,0 X
    1,2 O
    0,0 X
    2,2 O
    """

    play_move_script(g, script)

    assert_game_state(GameState.FINISHED, g.state)
    assert_result(Result.PLAYER2_VICTORY, g.result)


def test_player1_backslash_win():
    """Player 1 wins with a '\' sequence"""
    b = Board()
    g = Game(b)

    script = """
    1,1 X
    0,2 O
    1,0 X
    1,2 O
    2,2 X
    2,0 O
    0,0 X
    """

    play_move_script(g, script)

    assert_game_state(GameState.FINISHED, g.state)
    assert_result(Result.PLAYER1_VICTORY, g.result)


def test_player2_forwardslash_win():
    """Player 2 wins with a '/' sequence"""
    b = Board()
    g = Game(b)

    script = """
    0,0 X
    0,2 O
    1,0 X
    1,1 O
    0,1 X
    2,0 O
    """

    play_move_script(g, script)

    assert_game_state(GameState.FINISHED, g.state)
    assert_result(Result.PLAYER2_VICTORY, g.result)

def test_cat_game():
    b = Board()
    g = Game(b)

    script = """
    1,1 X
    0,0 O
    2,1 X
    0,1 O
    0,2 X
    2,0 O
    1,0 X
    1,2 O
    2,2 X
    """

    play_move_script(g, script)

    assert_game_state(GameState.FINISHED, g.state)
    assert_result(Result.CAT_GAME, g.result)

def test_at3():
    at3_data = """
[Event "World Tic-Tac-Toe Championships"]
[Site "Los Angeles, CA, USA"]
[Date "2025.02.21"]
[Player1 "Alice Kasparov"]
[Player2 "Bob Carlsen"]
[Result "Cat Game"]
[Player1Elo "3000"]
[Player2Elo "3000"]
[TimeControl "Whenever"]
[Grid "3x3"]
[Player1Choice "X"]
    
1. a1 2. b2
    """
    obj = parse(at3_data)
    print(obj)

def main():
    test_at3()

    ##test_player1_row_win()
    ##test_player2_col_win()
    ##test_player1_backslash_win()
    ##test_player2_forwardslash_win()
    ##test_cat_game()
    

if __name__ == "__main__":
    main()
