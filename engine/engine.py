from engine.game_tree import GameTree, MoveGenFn
from game.game import Game, GameEvent
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
        self.tree: GameTree | None = None

        if max_plies is None:
            self.max_plies = self.DEFAULT_PLIES
        else:
            self.max_plies = max_plies

    def generate_game_tree(self, fn: MoveGenFn) -> None:
        t = GameTree.generate(self.game, self.max_plies, fn)
        self.tree = t

    def listen_for_game_events(self) -> None:
        """Register a callback for anytime a move is made on the Game"""
        fn = self.on_game_event
        self.game.add_event_listener(fn)

    def on_game_event(self, evt: GameEvent) -> None:
        """Callback for anytime a GameEvent occurs"""
        pass

    def propose_move(self) -> Move:
        """Produce the next move"""
        raise NotImplementedError


def create_engine(
    cls: type[Engine], g: Game, p: Player, max_plies: int | None = None
) -> Engine:
    """Convenient factory function for creating an engine

    Importantly, this sets up move listening.
    """
    eng = cls(g, p, max_plies=max_plies)
    eng.listen_for_game_events()
    return eng
