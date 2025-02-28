import logging
from random import uniform

from engine.game_tree import Node
from game.game import GameState
from game.result import Result

logger = logging.getLogger(__name__)
DEBUG = logger.debug


def depth_penalty(depth: int, maximizer: bool, penalty=0.01) -> float:
    """
    How much each ply reduces the score, i.e. the sooner the win, the better
    """
    magnitude = penalty * (depth - 1)
    return -magnitude if maximizer else magnitude


def score_result(r: Result, victory=1.0) -> float:
    if r == Result.PLAYER1_VICTORY:
        return victory
    elif r == Result.PLAYER2_VICTORY:
        return -victory
    elif r == Result.DRAW:
        return 0.0
    else:
        raise Exception("unknown result")


def eval_end_state(cur_node: Node, depth: int, maximizer: bool) -> float:
    g = cur_node.game
    if g.state != GameState.FINISHED:
        return 0.0

    score = 0.0
    score += score_result(g.result)
    score += depth_penalty(depth, maximizer)

    return score


def eval_rand(cur_node: Node, depth: int, maximizer: bool) -> float:
    """This is in 'piece' units; so 2.0 is like player 1 having an extra
    piece. Likewise, -1.5 is like player 2 having the equivalent of an
    extra piece an a half.

    ~0.0 is considered draw-ish.
    """
    return uniform(-1.0, 1.0)
