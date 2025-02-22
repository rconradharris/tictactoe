from dataclasses import dataclass

from engine.placement_rule import PlacementRule
from engine.typedefs import BoardSize


@dataclass
class GameParameters:
    """
    GameParameters represent the low-level means by which games can vary.

    A higher-level GameChoice maps to fixed set of GameParameters.

    For example: Connect Four is rows=6, cols=7, win_count=4,
    PlacementRule.COLUMN_STACK
    """
    size: BoardSize
    win_count: int
    placement_rule: PlacementRule
