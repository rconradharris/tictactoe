from engine.engine import Engine
from engine.game_tree import EvalFn, MinimaxFn
from engine.minimax import minimax
from engine.mnk.heuristics import eval_rand


class Randimaxer(Engine):
    """Randimaxer is a game engine that uses the minimax algorithm to select
    moves but is rather stupid in that it uses an evaluation function which
    assigns a random score to each move.
    """

    DEFAULT_PLIES: int = 2
    EVAL_FN: EvalFn = eval_rand
    MINIMAX_FN: MinimaxFn = minimax
