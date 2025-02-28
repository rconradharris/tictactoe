from game.game import Game
from game.move import Move
from game.player import Player


class Engine:
    """
    Abstract base class for an engine capable of playing an m,n,k game
    """

    DEFAULT_PLIES = 2

    def __init__(self, g: Game, p: Player, max_plies: int | None = None) -> None:
        self.game = g
        self.player = p

        if max_plies is None:
            self.max_plies = self.DEFAULT_PLIES
        else:
            self.max_plies = max_plies

    def generate_move(self) -> Move:
        """Produce the next move"""
        raise NotImplementedError
