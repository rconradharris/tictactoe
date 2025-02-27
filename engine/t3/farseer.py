from engine.engine import Engine
from engine.minimax import best_node
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

    VICTORY_UNIT = 100.0
    DRAW_UNIT = 0.01

    def generate_move(self) -> Move:
        """Produce the next move"""
        fn = self._eval_optimal

        n = best_node(self.game, self.max_plies, fn)

        #print(f"{self.game.cur_player=} {n.move} {n.score=}")
        assert n.move is not None

        return n.move


    @classmethod
    def _eval_optimal(cls, g: Game, m: Move, depth: int) -> float:
        st = g.state
        r = g.result
        #print(f"{depth}: {m} {st=} {r=}")

        if st == GameState.FINISHED:
            if r == Result.PLAYER1_VICTORY:
                return (1 / depth) * cls.VICTORY_UNIT
            elif r == Result.PLAYER2_VICTORY:
                return (1 / depth) * -cls.VICTORY_UNIT
            elif r == Result.DRAW:
                p = g.cur_player
                if p == Player.P1:
                    return (1 / depth) * cls.DRAW_UNIT
                elif p == Player.P2:
                    return (1 / depth) * -cls.DRAW_UNIT
                else:
                    raise Exception('unknown player')
            else:
                raise Exception('unknown result')

        return 0.0
