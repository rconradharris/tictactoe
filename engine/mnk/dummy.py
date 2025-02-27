from random import choice

from engine.engine import Engine
from game.move import Move


class Dummy(Engine):
    """
    Dummy works by enumerating cells which constitute valid moves and then
    picking randomly from that list.

    In Tic-Tac-Toe, Dummy will pick from any empty cells on the board.

    In Connect Four, due to the COLUMN_STACK placement rule, Dummy will select
    from the top-most empty cells across the board.
    """

    def generate_move(self) -> Move:
        b = self.game.board
        cells = list(b.playable_cells())
        cell = choice(cells)
        return Move(cell, self.game.cur_piece)
