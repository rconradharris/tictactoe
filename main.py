from dataclasses import dataclass
import os

from at3.at3_object import AT3Object
from at3.parse import parse
from engine.board import Board
from engine.enums import GameState, Mark, Result
from engine.exceptions import MoveScriptBreak
from engine.game import Game
from engine.move import Move


@dataclass
class TestContext:
    description: str


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


def assert_game_state(t: TestContext, wanted: GameState, got: GameState):
    assert wanted == got, f"'{t.description}': {wanted=} {got=}"

def assert_result(t: TestContext, wanted: Result, got: Result):
    assert wanted == got, f"'{t.description}': {wanted=} as result, {got=} instead"

def assert_at3_result_ok(t: TestContext, obj: AT3Object, g: Game) -> None:
    """Ensure the game state matches what the AT3 result indicates"""
    assert_game_state(t, GameState.FINISHED, g.state)
    assert_result(t, obj.result, g.result)


def test_at3_case(path: str) -> None:
    with open(path) as f:
        at3_data = f.read()

    obj = parse(at3_data)

    b = Board(rows=obj.rows, cols=obj.cols)
    g = Game(b)

    for move in obj.moves:
        g.apply_move(move)
        show_board(g)

    t = TestContext(obj.event)

    assert_at3_result_ok(t, obj, g)


def test_at3_cases() -> None:
    TEST_CASES_PATH = 'tests/cases'
    filenames = os.listdir(TEST_CASES_PATH)
    filenames.sort()
    for filename in filenames:
        if not filename.endswith('.ttt'):
            continue

        path = os.path.join(TEST_CASES_PATH, filename)
        test_at3_case(path)


def main():
    test_at3_cases()
    

if __name__ == "__main__":
    main()
