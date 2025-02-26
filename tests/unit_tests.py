from game.board import Board
from game.move import Move
from game.placement_rule import PlacementRule
from game.piece import Piece


def test_top_empty_row():
    b = Board(
        size=(2, 2),
        win_count=2,
        placement_rule=PlacementRule.COLUMN_STACK
    )

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


def run_unit_tests():
    test_top_empty_row()
