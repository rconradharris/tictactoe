from engine.engine import Engine
from engine.game_tree import GameTree
from engine.minimax import minimax
from engine.mnk.heuristics import eval_rand
from game.game import generate_moves
from game.move import Move


class Randimaxer(Engine):
    """Randimaxer is a game engine that uses the minimax algorithm to select
    moves but is rather stupid in that it uses an evaluation function which
    assigns a random score to each move.
    """

    def generate_move(self) -> Move:
        """Produce the next move"""
        gFn = generate_moves
        t = GameTree.generate(self.game, self.max_plies, gFn)

        eFn = eval_rand
        mFn = minimax
        t.evaluate(self.max_plies, eFn, mFn)

        n = t.best_move()

        return n.move
