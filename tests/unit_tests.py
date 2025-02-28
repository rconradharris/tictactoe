from game.board import Board
from game.move import Move
from game.placement_rule import PlacementRule
from game.piece import Piece
from tests.context import TestContext
from tests.assertions import assert_cells


def test_top_empty_row():
    b = Board(size=(2, 2), win_count=2, placement_rule=PlacementRule.COLUMN_STACK)

    r = b.top_empty_row_for_column(0)
    assert r == 1

    m = Move((1, 0), Piece.X)
    b.apply_move(m)

    r = b.top_empty_row_for_column(0)
    assert r == 0

    m = Move((0, 0), Piece.X)
    b.apply_move(m)

    r = b.top_empty_row_for_column(0)
    assert r == -1


def test_playable_cells_column_stack():
    t = TestContext(
        description="test_playable_cells_column_stack",
    )

    b = Board(size=(2, 2), win_count=2, placement_rule=PlacementRule.COLUMN_STACK)

    got = list(b.playable_cells())
    wanted = [(1, 0), (1, 1)]
    assert_cells(t, wanted, got)

    m = Move((1, 0), Piece.X)
    b.apply_move(m)

    got = list(b.playable_cells())
    wanted = [(0, 0), (1, 1)]
    assert_cells(t, wanted, got)


def run_unit_tests():
    test_top_empty_row()
    test_playable_cells_column_stack()
