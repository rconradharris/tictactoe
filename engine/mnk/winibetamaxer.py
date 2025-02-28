from engine.alphabeta import alphabeta
from engine.engine import Engine
from engine.game_tree import GameTree
from engine.mnk.heuristics import eval_end_state
from game.move import Move


class Winibetamaxer(Engine):
    """
    Like Winimax but use alphabeta rather than simple minimax
    """
    DEFAULT_PLIES = 7

    def generate_move(self) -> Move:
        """Produce the next move"""
        t = GameTree(self.game)

        t.build(self.max_plies)

        eFn = eval_end_state
        mFn = alphabeta
        t.evaluate(self.max_plies, eFn, mFn)

        m, score = t.best_move()

        assert m is not None
        return m
