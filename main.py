from dataclasses import dataclass
import os
import sys

from at3.at3_object import AT3Object
from at3.file_extensions import valid_file_extension
from at3.parse import parse
from engine.board import Board
from engine.enums import GameState, Piece, Result
from engine.exceptions import IllegalMove
from engine.game import Game
from engine.game_choice import GameChoice
from engine.move import Move


@dataclass
class TestContext:
    description: str


def show_board(g: Game):
    print(f"{g.cur_player} {g.state} {g.result}")
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



def show_help() -> None:
    print("""\
GAME CHOICES
    T3 - Tic Tac Toe
    C4 - Connect Four

COMMANDS
    . - show board
    ? - display help

MOVE SYNTAX
    <column-letter><row-number> (ex: 'a1')""")


def game_loop(g: Game) -> None:
    CMD_SHOW_BOARD = "."
    CMD_HELP = "?"

    show_board(g)

    while True:
        piece_str = input('X or O? ')
        piece_str = piece_str.upper()
        try:
            cur_piece = Piece.from_str(piece_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    move_num = 1
    while True:
        if g.state == GameState.FINISHED:
            break

        cell_str = input(f"{move_num}. Move? ")

        if cell_str == CMD_SHOW_BOARD:
            show_board(g)
            continue
        elif cell_str == CMD_HELP:
            show_help()
            continue

        try:
            cell = Board.parse_algebraic_cell(cell_str)
        except ValueError as e:
            # Try again
            print(e)
            continue

        move = Move(cell, cur_piece)

        try:
            g.apply_move(move)
        except IllegalMove as e:
            # Try again
            print(e)
            continue

        show_board(g)

        move_num += 1
        cur_piece = cur_piece.next()

    print(g.result)


def interactive() -> None:
    while True:
        choice_str = input('Tic-Tac-Toe or Connect Four (T3 or C4)? ')
        try:
            choice = GameChoice.from_abbrev(choice_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    b = Board()

    params = choice.parameters()
    if params:
        b = Board(
            rows=params.rows,
            cols=params.cols,
            win_count=params.win_count,
            placement_rule=params.placement_rule
        )

    g = Game(b)

    game_loop(g)


def main():
    if len(sys.argv) < 2:
        print("usage: main.py <play|test>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "play":
        interactive()
    elif cmd == "test":
        run_tests('tests')
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)
    #run_tests('tests/c4')
    #run_test("tests/c4/000_p1_row_win.c4")
    

if __name__ == "__main__":
    main()
