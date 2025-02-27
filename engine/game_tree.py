import logging
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import List, Optional, Tuple

from game.game import Game, GameState
from game.move import Move
from game.player import Player


logger = logging.getLogger(__name__)
INFO = logger.info


type EvalFn = Callable[[Game, Move, int], float]


def is_maximizer(p: Player) -> bool:
    """Player 1 is always the maximizer

    +1.0 is an immediate player 1 victory
    -1.0 is an immediate player 2 victory
     0.0 is an immediate draw
    """
    return p == Player.P1


@dataclass
class Node:
    """A game tree node for use in a minimax algorithm"""
    tree: 'GameTree' = field(repr=False)
    game: Game = field(repr=False)
    move: Move | None = None
    parent: Optional['Node'] = None
    depth: int  = 0
    # Use None instead of 0.0 so we can easily detect if minimax didn't fill
    # the node in with a score
    score: float | None = None

    children: List['Node'] = field(default_factory=list, repr=True)

    @property
    def maximizer(self) -> bool:
        return is_maximizer(self.game.cur_player)

    def pretty(self) -> str:
        if self.move:
            m = self.move.pretty()
        else:
            m = "ROOT"
        return f"{m} ({self.score:.3f})"

    def add_child(self, child: 'Node') -> None:
        self.children.append(child)
        self.tree.size += 1

    def set_score(self, score: float) -> None:
        self.score = score
        self.tree.scored += 1


@dataclass
class GameTree:
    root: Node

    # Number of nodes in the tree
    size: int = 0

    # The number of nodes that have been scored (i.e. visited)
    # Reducing max_plies reduces the number of nodes visited
    scored: int = 0

    def __init__(self, g: Game) -> None:
        self.root = Node(self, g.copy())
        self.size += 1

    def build(self, max_plies: int) -> None:
        """Build out the subtree underneath the root"""
        _build_subtree(self.root, max_plies)

    def evaluate(self, max_plies: int, fn: EvalFn) -> None:
        """Place the evaluation minimaxer code in here"""
        raise NotImplementedError

    def best_move(self) -> Tuple[Move, float]:
        children = self.root.children

        scores = []
        for idx, child in enumerate(children):
            scores.append((child.score, idx))

        if self.root.maximizer:
            scores.sort(reverse=True)
        else:
            scores.sort()

        best_score, best_idx = scores[0]
        best_node = children[best_idx]

        pretty_scores = [children[idx].pretty() for _, idx in scores]
        INFO(f"best: {best_node.pretty()} {pretty_scores}")

        assert best_node.move is not None
        assert best_node.score is not None

        return (best_node.move, best_node.score)


def _build_subtree(cur_node: Node, num_plies: int) -> None:
    if num_plies == 0:
        return

    g = cur_node.game

    if cur_node.move:
        assert cur_node.move.piece == g.cur_piece

    if cur_node.move and g.state != GameState.FINISHED:
        g.apply_move(cur_node.move)

    if g.state == GameState.FINISHED:
        return

    p = g.cur_piece

    if cur_node.move:
        cur_node_piece = cur_node.move.piece
        assert p != cur_node.move.piece, \
                f"{p=} should not equal {cur_node_piece=}"


    for cell in g.board.playable_cells():
        m = Move(cell, p)

        child = Node(tree=cur_node.tree,
                     game=g.copy(),
                     move=m,
                     parent=cur_node,
                     depth=cur_node.depth + 1)

        cur_node.add_child(child)

        _build_subtree(child, num_plies - 1)
