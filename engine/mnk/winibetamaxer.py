from engine.alphabeta import alphabeta
from engine.engine import Engine
from engine.mnk.heuristics import eval_end_state
from game.game import generate_moves
from game.move import Move


class Winibetamaxer(Engine):
    """
    Like Winimax but use alphabeta rather than simple minimax
    """

    DEFAULT_PLIES = 7

    def propose_move(self) -> Move:
        """Produce the next move"""
        gFn = generate_moves
        self.generate_game_tree(gFn)
        t = self.tree
        assert t is not None

        eFn = eval_end_state
        mFn = alphabeta
        t.evaluate(self.max_plies, eFn, mFn)

        n = t.best_move()

        return n.move
