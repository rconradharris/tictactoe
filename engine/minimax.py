from collections.abc import Callable
from dataclasses import dataclass, field
from typing import List

from game.game import Game
from game.move import Move
from game.player import Player


type EvalFn = Callable[[Game, Move], float]


def best_move(g: Game, max_plies: int, fn: EvalFn) -> Move:
    """Return the current player's best move according to the evaluation
    function
    """
    t = GameTree.from_game(g, max_plies)
    maximizer = g.cur_player == Player.P1

    minimax(t.root, 3, maximizer, fn)

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
    assert best_node.move is not None
    return best_node.move


@dataclass
class Node:
    """A game tree node for use in a minimax algorithm"""
    game: Game = field(repr=False)
    move: Move | None = None
    score: float = 0.0

    children: List['Node'] = field(default_factory=list)




def _build_subtree(cur_node: Node, num_plies: int) -> None:
    if num_plies == 0:
        return

    g = cur_node.game

    if cur_node.move:
        g.apply_move(cur_node.move)

    p = g.cur_piece

    for cell in g.board.playable_cells():
        m = Move(cell, p)
        child = Node(g.copy(), m)
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
        score = fn(node.game, node.move)
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
