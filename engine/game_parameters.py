from dataclasses import dataclass

from engine.placement_rule import PlacementRule
from engine.typedefs import BoardSize


@dataclass
class GameParameters:
    size: BoardSize
    win_count: int
    placement_rule: PlacementRule
