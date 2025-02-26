from typing import List
from at3.at3_object import AT3Object
from game.game import Game, GameState
from game.result import Result
from game.typedefs import Cell
from tests.context import TestContext


def assert_game_state(t: TestContext, wanted: GameState, got: GameState):
    assert wanted == got, f"'{t.description}': {wanted=} {got=}"


def assert_result(t: TestContext, wanted: Result, got: Result):
    assert wanted == got, f"'{t.description}': {wanted=} as result, {got=} instead"


def assert_game_result_matches_file(t: TestContext, obj: AT3Object, g: Game) -> None:
    """Assert that the Result associated with the Game matches the Result
    declared by the AT3 file.
    """
    non_terminal = (Result.UNDEFINED, Result.UNFINISHED)

    if obj.result not in non_terminal:
        assert_game_state(t, GameState.FINISHED, g.state)
        assert_result(t, obj.result, g.result)


def assert_cells(t: TestContext, wanted: List[Cell], got: List[Cell]) -> None:
    assert wanted == got, f"'{t.description}': {wanted=} , {got=} instead"
