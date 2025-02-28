import logging

from engine.game_tree import EvalFn, Node


logger = logging.getLogger(__name__)


def _alphabeta(
    node: Node, depth: int, alpha: float, beta: float, maximizer: bool, fn: EvalFn
) -> float:
    """Apply the minimax algorithm to the game tree with alpha beta pruning."""
    # Leaf (or hit depth stop)
    if depth == 0 or len(node.children) == 0:
        assert node.move is not None
        score = fn(node.game, node.move, node.depth)
        node.set_score(score)
        return score

    # Maximizer
    if maximizer:
        value = float("-inf")
        for child in node.children:
            value = max(value, _alphabeta(child, depth - 1, alpha, beta, False, fn))
            if value > beta:
                break  # beta pruning

        node.set_score(value)
        return value

    # Minimizer
    value = float("inf")
    for child in node.children:
        value = min(value, _alphabeta(child, depth - 1, alpha, beta, True, fn))

        if value < alpha:
            break  # alpha pruning

    node.set_score(value)
    return value


def alphabeta(node: Node, depth: int, maximizer: bool, fn: EvalFn) -> float:
    """Kickoff function for minimax with alpha beta pruning"""
    alpha = float("-inf")
    beta = float("inf")
    return _alphabeta(node, depth, alpha, beta, maximizer, fn)
