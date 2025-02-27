from engine.engine import Engine
from engine.minimax import MinimaxTree
from game.game import Game, GameState
from game.move import Move
from game.player import Player
from game.result import Result


class T3Farseer(Engine):
    """
    Farseer is slow but accurate.

    It works by looking far ahead. This makes the search slow since the number
    of search space grows exponentially with the number of plies.
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

        fn = self._eval_optimal
        t.evaluate(self.max_plies, fn)

        m, score = t.best_move()

        assert m is not None
        return m

    @classmethod
    def _eval_optimal(cls, g: Game, m: Move, depth: int) -> float:
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

        #print(f"{depth}: {m} {st=} {r=} {pen=}")

        # Reduce the value of a victory if its more plies away
        pen = cls.DEPTH_PENALTY * (depth - 1)
        score -= pen

        if g.cur_player == Player.P2:
            # Player 2 is always the minimizer
            score = -score

        return score
