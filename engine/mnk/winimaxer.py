from engine.engine import Engine
from engine.game_tree import GameTree
from engine.minimax import minimax
from engine.mnk.heuristics import eval_end_state
from game.game import generate_moves
from game.move import Move


class Winimaxer(Engine):
    """
    Winimaxer applies the naive minimax algorithm to search the game tree for
    wins and draws.

    Winimax doesn't use a heuristic, it strictly look for wins and draws. That
    means, if a the game doesn't terminate within its search horizon, it
    considers all moves to be effectively draws.

    This often leads to it choosing suboptimal moves.

    An improvement would be to use a heuristic to select more promising moves,
    like picking cells with more neighbors and picking cells that increase the
    `run_count`.

    All that said, if you make `max_plies` large enough so that the search
    horizon is the entire game tree, Winimax is guaranteed to play optimally
    (and very slowly).
    """

    DEFAULT_PLIES = 7

    def propose_move(self) -> Move:
        """Produce the next move"""
        gFn = generate_moves
        t = GameTree.generate(self.game, self.max_plies, gFn)

        eFn = eval_end_state
        mFn = minimax
        t.evaluate(self.max_plies, eFn, mFn)

        n = t.best_move()

        return n.move
