import os

from at3.file_extensions import valid_file_extension
from at3.parse import parse
from game.board import Board
from game.game import Game
from tests.assertions import assert_game_result_matches_file
from tests.context import TestContext


def _show_board(g: Game):
    print(f"{g.cur_player} {g.state} {g.result}")
    print(g.board.pretty(coords=True))
    print()


def run_file_test(path: str) -> None:
    with open(path) as f:
        at3_data = f.read()

    try:
        obj = parse(at3_data, path=path)
    except Exception as e:
        print(f"{path}: test failure")
        raise e

    b = Board(size=obj.size, win_count=obj.win_count, placement_rule=obj.placement_rule)

    g = Game(b)
    g.choose_player1_piece(obj.player1_piece)

    t = TestContext(obj.event)

    _show_board(g)
    for move in obj.moves:
        try:
            g.apply_move(move)
        except Exception as e:
            print(f"{t.description}: test failure")
            raise e

        _show_board(g)

    assert_game_result_matches_file(t, obj, g)


def run_file_tests(root: str) -> None:
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
            run_file_test(path)
