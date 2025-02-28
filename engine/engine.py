from engine.alphabeta import alphabeta
from engine.game_tree import EvalFn, GameTree, MoveGenFn, MinimaxFn
from engine.mnk.heuristics import eval_end_state
from game.game import Game, GameEvent, generate_moves
from game.move import Move
from game.player import Player


class Engine:
    """
    Abstract base class for an engine capable of playing an m,n,k game
    """

    DEFAULT_PLIES: int = 2
    EVAL_FN: EvalFn = eval_end_state
    MINIMAX_FN: MinimaxFn = alphabeta

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
        gFn = generate_moves
        self.generate_game_tree(gFn)

        t = self.tree

        assert t is not None

        # If we access these function using `self` then it will be treated as
        # a bound method and we'll have `self` passsed in implicitly which is
        # not what we want. Referencing it via a class member avoids binding
        # the function to the instance so the function arity is unchanged
        cls = self.__class__
        eFn = cls.EVAL_FN
        mFn = cls.MINIMAX_FN

        t.evaluate(self.max_plies, eFn, mFn)

        n = t.best_move()

        return n.move


def create_engine(
    cls: type[Engine], g: Game, p: Player, max_plies: int | None = None
) -> Engine:
    """Convenient factory function for creating an engine

    Importantly, this sets up move listening.
    """
    eng = cls(g, p, max_plies=max_plies)
    eng.listen_for_game_events()
    return eng
