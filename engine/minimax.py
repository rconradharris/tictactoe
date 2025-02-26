from dataclasses import dataclass, field
from typing import List

from game.game import Game
from game.move import Move


@dataclass
class Node:
    """A game tree node for use in a minimax algorithm"""
    move: Move | None = None

    children: List['Node'] = field(default_factory=list)

    def heuristic(self) -> float:
        """This is in 'piece' units; so 2.0 is like player 1 having an extra
        piece. Likewise, -1.5 is like player 2 having the equivalent of an
        extra piece an a half.

        ~0.0 is considered draw-ish.
        """
        return 0.0

    def terminal(self) -> bool:
        return len(self.children) == 0


def node_walk(cur_node: Node, g: Game, num_plies: int) -> None:
    if num_plies == 0:
        return

    g = g.copy()  # Preserve the original game state

    if cur_node.move:
        g.apply_move(cur_node.move)

    p = g.cur_piece

    for cell in g.board.playable_cells():
        m = Move(cell, p)
        #print(f"{num_plies=} {m=}")
        child = Node(m)
        cur_node.children.append(child)

        node_walk(child, g, num_plies - 1)


@dataclass
class GameTree:
    root: Node

    @classmethod
    def from_game(cls, g: Game, num_plies: int) -> 'GameTree':
        root = Node()
        t = GameTree(root)
        node_walk(root, g, num_plies)
        return t


def minimax(node: Node, depth: int, maximizer: bool) -> float:
    if depth == 0 or node.terminal():
        return node.heuristic()

    if maximizer:
        maxv = float('-inf')
        for child in node.children:
            maxv = max(maxv, minimax(child, depth - 1, False))
        return maxv

    # Minimizer
    minv = float('inf')
    for child in node.children:
        minv = min(minv, minimax(child, depth - 1, True))

    return minv
