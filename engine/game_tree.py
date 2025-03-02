import logging
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Generator, List

from game.game import Game, GameState
from game.move import Move, NULL_MOVE
from game.player import Player


logger = logging.getLogger(__name__)
INFO = logger.info


# This function evaluates the position after a given move
#
# fn(node, depth, maximizer) -> score
type EvalFn = Callable[[Node, int, bool], float]

# This function applies minimax (or a variant) to the game tree
#
# fn(node, depth, maximizer, evalFn) -> score
type MinimaxFn = Callable[[Node, int, bool, EvalFn], float]

# A move generator is a function that given a Game produces Moves
#
# It's more efficient if the move generator emits promising moves first
#
# fn(game) -> Gen(Move, ...)
type MoveGenFn = Callable[[Game], Generator[Move]]


@dataclass
class Node:
    """A game tree node for use in a minimax algorithm"""

    game: Game = field(repr=False)
    move: Move

    # Use None instead of 0.0 so we can easily detect if minimax didn't fill
    # the node in with a score
    score: float | None = None

    children: List["Node"] = field(default_factory=list, repr=True)

    def is_root(self) -> bool:
        """Return True if this is a root node.

        Root nodes are represent the current game state and have a null move
        """
        return self.move is NULL_MOVE

    def is_maximizer(self) -> bool:
        """Player 1 is always the maximizer

        > 0.0 player 1 advantage
        < 0.0 player 2 advantage
        = 0.0 is draw-ish
        """
        g = self.game
        return g.cur_player == Player.P1

    def pretty(self) -> str:
        if self.move is NULL_MOVE:
            m = "ROOT"
        else:
            m = self.move.pretty()
        return f"{m} ({self.score:.3f})"

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def set_score(self, score: float) -> None:
        self.score = score


@dataclass
class GameTree:
    root: Node

    def build(self, max_plies: int, fn: MoveGenFn) -> None:
        """Build out the subtree underneath the root"""
        _build_subtree(self.root, max_plies, fn)

    def evaluate(self, max_plies: int, eFn: EvalFn, mFn: MinimaxFn) -> float:
        """Evaluate the game tree using minimax"""
        r = self.root
        maximizer = r.is_maximizer()
        return mFn(r, max_plies, maximizer, eFn)

    def best_move(self) -> Node:
        """Return the node for the best move"""
        children = self.root.children

        scores = []
        for idx, child in enumerate(children):
            scores.append((child.score, idx))

        if self.root.is_maximizer():
            scores.sort(reverse=True)
        else:
            scores.sort()

        best_score, best_idx = scores[0]
        best_node = children[best_idx]

        pretty_scores = [children[idx].pretty() for _, idx in scores]
        INFO(f"best: {best_node.pretty()} {pretty_scores}")

        return best_node

    @classmethod
    def generate(cls, g: Game, max_plies: int, move_generator: MoveGenFn) -> "GameTree":
        """Convenient factory function for building out a GameTree"""
        root = Node(g.copy(), NULL_MOVE)
        t = GameTree(root)
        t.build(max_plies, move_generator)
        return t


def _build_subtree(cur_node: Node, num_plies: int, move_generator: MoveGenFn) -> None:
    """Recursively build out the tree

    :param cur_node: the node we're currently visiting
    :param num_plies: number of plies remaining in our depth stop
    :param move_generator: A function to generate promising moves in a game
    """
    if num_plies == 0:
        return

    g = cur_node.game

    is_root = cur_node.is_root()

    if not is_root:
        g_p = g.cur_piece
        n_p = cur_node.move.piece
        assert cur_node.move.piece == g.cur_piece, f"{n_p=} != {g_p=}"

        if g.state != GameState.FINISHED:
            g.apply_move(cur_node.move)

    if g.state == GameState.FINISHED:
        return

    p = g.cur_piece

    if not is_root:
        cur_node_piece = cur_node.move.piece
        assert p != cur_node.move.piece, f"{p=} should not equal {cur_node_piece=}"

    for m in move_generator(g):
        child = Node(g.copy(), m)
        cur_node.add_child(child)

        _build_subtree(child, num_plies - 1, move_generator)
