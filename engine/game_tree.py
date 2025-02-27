from dataclasses import dataclass, field
from collections.abc import Callable
from typing import List, Optional, Tuple

from game.game import Game, GameState
from game.move import Move
from game.player import Player


type EvalFn = Callable[[Game, Move, int], float]


@dataclass
class Node:
    """A game tree node for use in a minimax algorithm"""
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
        """Player 1 is always the maximizer

        +1.0 is a player 1 victory
        -1.0 is a player 2 victory
         0.0 is a draw
        """
        return self.game.cur_player == Player.P1

    def pretty(self) -> str:
        if self.move:
            m = self.move.pretty()
        else:
            m = "ROOT"
        return f"{m} ({self.score:.3f})"


@dataclass
class GameTree:
    root: Node

    def __init__(self, g: Game) -> None:
        self.root = Node(g.copy())

    def build(self, max_plies: int) -> None:
        """Build out the subtree underneath the root"""
        _build_subtree(self.root, max_plies)

    def evaluate(self, max_plies: int, fn: EvalFn) -> None:
        """Place the evaluation minimaxer code in here"""
        raise NotImplementedError

    def best_move(self, verbose: bool = False) -> Tuple[Move, float]:
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

        if verbose:
            pretty_scores = [children[idx].pretty() for _, idx in scores]
            print(f"best: {best_node.pretty()} {pretty_scores}")

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

        child = Node(game=g.copy(),
                     move=m,
                     parent=cur_node,
                     depth=cur_node.depth + 1)

        cur_node.children.append(child)
        _build_subtree(child, num_plies - 1)
