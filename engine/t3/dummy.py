from engine.engine import Engine
from game.move import Move
from game.piece import Piece

class Dummy(Engine):
    """
    A dummy is an engine that selects a random move and attempts to play it
    without regard to whether the move is legal or good.

    If the move is illegal, the dummy will try another random move.

    The only sensibility of dummy is to not play the same move twice.
    """

    def move(self) -> Move:
        # TODO: fill this out...
        return Move(0, 0, Piece.X)
