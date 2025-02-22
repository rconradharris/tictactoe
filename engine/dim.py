"""
Utilities for working in higher dimensions
"""
from typing import List


def within_bounds(coords: List[int],
                  lower_bounds: List[int],
                  upper_bounds: List[int]) -> bool:
    """Returns True if the coord in N-dimensional space is within the range of
    [lower_bound, upper_bound)
    """
    assert len(coords) == len(lower_bounds)
    assert len(lower_bounds) == len(upper_bounds)

    for coord, lb, ub in zip(coords, lower_bounds, upper_bounds):
        within_bounds = lb <= coord < ub
        if not within_bounds:
            return False

    return True
