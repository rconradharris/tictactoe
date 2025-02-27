from random import uniform

from engine.engine import Engine
from engine.minimax import MinimaxTree
from game.game import Game
from game.move import Move


class Randimaxer(Engine):
    """Randimaxer is a game engine that uses the minimax algorithm to select
    moves but is rather stupid in that it uses an evaluation function which
    assigns a random score to each move.
    """

    def generate_move(self) -> Move:
        """Produce the next move"""
        t = MinimaxTree(self.game)

        t.build(self.max_plies)

        t.evaluate(self.max_plies, _eval_rand)

        m, score = t.best_move()

        assert m is not None
        return m


def _eval_rand(g: Game, m: Move, depth: int) -> float:
    """This is in 'piece' units; so 2.0 is like player 1 having an extra
    piece. Likewise, -1.5 is like player 2 having the equivalent of an
    extra piece an a half.

    ~0.0 is considered draw-ish.
    """
    return uniform(-1.0, 1.0)
