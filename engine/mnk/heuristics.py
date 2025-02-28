from random import uniform

from engine.game_tree import is_maximizer
from game.game import Game, GameState
from game.move import Move
from game.result import Result

# Score for a victory on the next move
VICTORY_UNIT = 1.0

DRAW_UNIT = 0.0

# How much each ply reduces the score, i.e. the sooner the win, the better
DEPTH_PENALTY = 0.01


def eval_end_state(g: Game, m: Move, depth: int) -> float:
    if g.state != GameState.FINISHED:
        return DRAW_UNIT

    score = DRAW_UNIT

    r = g.result
    if r == Result.PLAYER1_VICTORY:
        score = VICTORY_UNIT
    elif r == Result.PLAYER2_VICTORY:
        score = VICTORY_UNIT
    elif r == Result.DRAW:
        score = DRAW_UNIT
    else:
        raise Exception("unknown result")

    # Reduce the value of a victory if it takes more moves to get there
    pen = DEPTH_PENALTY * (depth - 1)
    score -= pen

    maximizer = is_maximizer(g.cur_player)
    if not maximizer:
        score = -score

    return score


def eval_rand(g: Game, m: Move, depth: int) -> float:
    """This is in 'piece' units; so 2.0 is like player 1 having an extra
    piece. Likewise, -1.5 is like player 2 having the equivalent of an
    extra piece an a half.

    ~0.0 is considered draw-ish.
    """
    return uniform(-1.0, 1.0)
