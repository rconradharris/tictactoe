from engine.engine import Engine
from engine.game_tree import is_maximizer
from engine.minimax import MinimaxTree
from game.game import Game, GameState
from game.move import Move
from game.result import Result


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

    # Score for a victory on the next move
    VICTORY_UNIT = 1.0

    DRAW_UNIT = 0.0

    # How much each ply reduces the score, i.e. the sooner the win, the better
    DEPTH_PENALTY = 0.01

    def generate_move(self) -> Move:
        """Produce the next move"""
        t = MinimaxTree(self.game)

        t.build(self.max_plies)

        fn = self._eval_end_state
        t.evaluate(self.max_plies, fn)

        m, score = t.best_move()

        assert m is not None
        return m

    @classmethod
    def _eval_end_state(cls, g: Game, m: Move, depth: int) -> float:
        if g.state != GameState.FINISHED:
            return cls.DRAW_UNIT

        score = cls.DRAW_UNIT

        r = g.result
        if r == Result.PLAYER1_VICTORY:
            score = cls.VICTORY_UNIT
        elif r == Result.PLAYER2_VICTORY:
            score = cls.VICTORY_UNIT
        elif r == Result.DRAW:
            score = cls.DRAW_UNIT
        else:
            raise Exception('unknown result')

        # Reduce the value of a victory if it takes more moves to get there
        pen = cls.DEPTH_PENALTY * (depth - 1)
        score -= pen

        maximizer = is_maximizer(g.cur_player)
        if not maximizer:
            score = -score

        return score
