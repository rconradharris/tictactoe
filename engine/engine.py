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

    def listen_for_moves(self) -> None:
        """Register a callback for anytime a move is made on the Game"""
        fn = self.move_applied
        self.game.add_move_listener(fn)

    def move_applied(self, m: Move) -> None:
        """Callback for anytime a move is made in the game"""
        pass

    def propose_move(self) -> Move:
        """Produce the next move"""
        raise NotImplementedError


def create_engine(
    cls: type[Engine], g: Game, p: Player, max_plies: int | None
) -> Engine:
    """Convenient factory function for creating an engine

    Importantly, this sets up move listening.
    """
    eng = cls(g, p, max_plies=max_plies)
    eng.listen_for_moves()
    return eng
