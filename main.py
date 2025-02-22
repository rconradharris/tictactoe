from dataclasses import dataclass
import os

from at3.at3_object import AT3Object
from at3.file_extensions import valid_file_extension
from at3.parse import parse
from engine.board import Board
from engine.enums import GameState, Result
from engine.game import Game


@dataclass
class TestContext:
    description: str


def show_board(g: Game):
    print(f"{g.cur_player=} {g.state=} {g.result}")
    print(g.board.pretty(coords=True))
    print()


def assert_game_state(t: TestContext, wanted: GameState, got: GameState):
    assert wanted == got, f"'{t.description}': {wanted=} {got=}"


def assert_result(t: TestContext, wanted: Result, got: Result):
    assert wanted == got, f"'{t.description}': {wanted=} as result, {got=} instead"


def assert_at3_result_ok(t: TestContext, obj: AT3Object, g: Game) -> None:
    """Ensure the game state matches what the AT3 result indicates"""
    non_terminal = (Result.UNDEFINED, Result.UNFINISHED)

    if obj.result not in non_terminal:
        assert_game_state(t, GameState.FINISHED, g.state)
        assert_result(t, obj.result, g.result)


def run_test(path: str) -> None:
    with open(path) as f:
        at3_data = f.read()

    obj = parse(at3_data, path=path)

    b = Board(rows=obj.rows,
              cols=obj.cols,
              win_count=obj.win_count,
              placement_rule=obj.placement_rule)

    g = Game(b)

    t = TestContext(obj.event)

    show_board(g)
    for move in obj.moves:
        try:
            g.apply_move(move)
        except Exception as e:
            print(f"{t.description}: test failure")
            raise e

        show_board(g)


    assert_at3_result_ok(t, obj, g)


def run_tests(root: str) -> None:
    # Collect test files
    test_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            test_files.append(path)

    # Sort for stability
    test_files.sort()

    # Run tests
    for path in test_files:
        if valid_file_extension(path):
            run_test(path)


def main():
    run_tests('tests')
    #run_tests('tests/c4')
    #run_test("tests/c4/000_p1_row_win.c4")
    

if __name__ == "__main__":
    main()
