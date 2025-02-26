from game.game import Game
from game.move import Move
from game.player import Player

class Engine:
    """
    Abstract base class for an engine capable of playing tic-tac-toe.
    """
    def __init__(self, g: Game, p: Player) -> None:
        """
        :param g: The game object
        :param p: Which player the computer is
        """
        self.game: Game = g
        self.player : Player = p

    def generate_move(self) -> Move:
        """Produce the next move"""
        raise NotImplementedError
