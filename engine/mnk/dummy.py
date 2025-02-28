from random import choice

from engine.engine import Engine
from engine.game_tree import MoveGenFn
from game.game import generate_moves
from game.move import Move


class Dummy(Engine):
    """
    Dummy works by enumerating cells which constitute valid moves and then
    picking randomly from that list.

    In Tic-Tac-Toe, Dummy will pick from any empty cells on the board.

    In Connect Four, due to the COLUMN_STACK placement rule, Dummy will select
    from the top-most empty cells across the board.
    """

    def generate_game_tree(self, fn: MoveGenFn) -> None:
        """The Dummy engine doesn't use a Game Tree"""
        pass

    def propose_move(self) -> Move:
        moves = list(generate_moves(self.game))
        return choice(moves)
