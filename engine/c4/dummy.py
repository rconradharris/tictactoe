from random import choice
from typing import List

from engine.engine import Engine
from game.game import Game
from game.move import Move
from game.piece import Piece
from game.player import Player
from game.typedefs import Cell


class C4Dummy(Engine):
    """
    The Dummy engine plays a move to a random column with at least one
    unoccupied cell remaining
    """
    def _playable_columns(self) -> List[int]:
        """Returns columns with at least one unoccupied cell remaining"""
        g = self.game
        b = g.board
        rows, cols = g.board.size

        playable_cols: List[int] = []

        # Most efficient to scan column-wise, bottom up
        for col in range(cols):
            for row_one_indexed in range(rows, 1, -1):
                row = row_one_indexed - 1  # Zero indexed
                cell = (row, col)
                p = b.cell_value(cell)
                if p == Piece._:
                    playable_cols.append(col)

        return playable_cols

    def generate_move(self) -> Move:
        b = self.game.board

        playable_cols = self._playable_columns()
        col = choice(playable_cols)

        row = b.top_empty_row_for_column(col)
        cell = (row, col)

        return Move(cell, self.game.cur_piece)
