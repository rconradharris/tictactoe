from engine.alphabeta import alphabeta
from engine.engine import Engine
from engine.game_tree import MinimaxFn


class Winibetamaxer(Engine):
    """
    Like Winimax but use alphabeta rather than simple minimax
    """

    DEFAULT_PLIES: int = 7

    MINIMAX_FN: MinimaxFn = alphabeta
