from dataclasses import dataclass

from game.game import Game
from game.move import Move
from game.player import Player

@dataclass
class Engine:
    """
    Abstract base class for an engine capable of playing an m,n,k game
    """
    DEFAULT_PLIES = 2

    game: Game
    player: Player
    max_plies: int = DEFAULT_PLIES

    def generate_move(self) -> Move:
        """Produce the next move"""
        raise NotImplementedError
