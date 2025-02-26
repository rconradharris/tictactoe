from random import choice

from engine.engine import Engine
from game.move import Move


class T3Dummy(Engine):
    """
    The Dummy engine plays a move to a random blank cell.
    """
    def generate_move(self) -> Move:
        b = self.game.board
        cells = list(b.playable_cells())
        cell = choice(cells)
        return Move(cell, self.game.cur_piece)
