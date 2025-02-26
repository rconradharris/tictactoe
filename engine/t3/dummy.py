from random import choice
from typing import List

from engine.engine import Engine
from game.game import Game
from game.move import Move
from game.piece import Piece
from game.player import Player
from game.typedefs import Cell


class T3Dummy(Engine):
    """
    The Dummy engine plays a move to a random blank cell.
    """
    def _blank_cells(self) -> List[Cell]:
        g = self.game
        b = g.board
        rows, cols = g.board.size

        blanks: List[Cell] = []

        for row in range(rows):
            for col in range(cols):
                cell = (row, col)
                p = b.cell_value(cell)
                if p == Piece._:
                    blanks.append(cell)

        return blanks

    def generate_move(self) -> Move:
        blanks = self._blank_cells()
        cell = choice(blanks)
        return Move(cell, self.game.cur_piece)
