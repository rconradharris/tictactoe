from engine.engine import Engine
from engine.game_tree import MinimaxFn
from engine.minimax import minimax


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

    DEFAULT_PLIES: int = 7

    # Use naive minimax w/o alpha/beta pruning
    MINIMAX_FN: MinimaxFn = minimax
