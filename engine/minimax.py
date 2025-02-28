import logging

from engine.game_tree import EvalFn, Node


logger = logging.getLogger(__name__)


def minimax(node: Node, depth: int, maximizer: bool, fn: EvalFn) -> float:
    """Apply the minimax algorithm to the game tree.

    This involves visiting each node and:

    1. If the node is a leaf, running an eval function to 'score' the game
    after the given move was played.

    2. If we're an internal node, then we assign our score based on the min or
    the max of our children depending on whether we're the minimizer or the
    maximizer.
    """
    # Leaf (or hit depth stop)
    if depth == 0 or len(node.children) == 0:
        assert node.move is not None
        score = fn(node, depth, maximizer)
        node.set_score(score)
        return score

    # Maximizer
    if maximizer:
        maxv = float("-inf")
        for child in node.children:
            maxv = max(maxv, minimax(child, depth - 1, False, fn))
        node.set_score(maxv)
        return maxv

    # Minimizer
    minv = float("inf")
    for child in node.children:
        minv = min(minv, minimax(child, depth - 1, True, fn))
    node.set_score(minv)
    return minv
