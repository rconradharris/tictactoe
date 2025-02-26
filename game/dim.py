"""
Utilities for working in higher dimensions
"""
from typing import List


type Dim = List[int]
type Point = List[int]


def within_bounds(coords: Point, lower_bounds: Dim, upper_bounds: Dim) -> bool:
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
