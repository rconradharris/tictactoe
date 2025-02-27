from collections.abc import Callable
from dataclasses import dataclass, field
from typing import List, Optional

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

    def pretty(self) -> str:
        if self.move:
            m = self.move.pretty()
        else:
            m = "ROOT"
        return f"{m} ({self.score:.3f})"


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


@dataclass
class GameTree:
    root: Node

    @classmethod
    def from_game(cls, g: Game, max_plies: int) -> 'GameTree':
        root = Node(g.copy())
        t = GameTree(root)
        _build_subtree(root, max_plies)
        return t


def minimax(node: Node, depth: int, maximizer: bool, fn: EvalFn) -> float:
    # Leaf (or hit depth stop)
    if depth == 0 or len(node.children) == 0:
        assert node.move is not None
        score = fn(node.game, node.move, node.depth)
        node.score = score
        return score

    # Maximizer
    if maximizer:
        maxv = float('-inf')
        for child in node.children:
            maxv = max(maxv, minimax(child, depth - 1, False, fn))
        node.score = maxv
        return maxv

    # Minimizer
    minv = float('inf')
    for child in node.children:
        minv = min(minv, minimax(child, depth - 1, True, fn))
    node.score = minv
    return minv


def best_node(g: Game, max_plies: int, fn: EvalFn,
              verbose: bool = True) -> Node:
    """Return the current player's best move according to the evaluation
    function
    """
    t = GameTree.from_game(g, max_plies)
    maximizer = g.cur_player == Player.P1

    #if verbose:
    #    print("= Before minimax =")
    #    pprint(t)

    minimax(t.root, max_plies, maximizer, fn)

    #if verbose:
    #    print("= After minimax =")
    #    pprint(t)

    n = t.root
    scores = []
    for idx, child in enumerate(n.children):
        scores.append((child.score, idx))

    if maximizer:
        scores.sort(reverse=True)
    else:
        scores.sort()

    best_score, best_idx = scores[0]
    best_node = n.children[best_idx]

    if verbose:
        m = best_node.move
        assert m is not None
        pretty_scores = [n.children[idx].pretty() for _, idx in scores]
        print(f"best: {best_node.pretty()} {pretty_scores}")

    return best_node
