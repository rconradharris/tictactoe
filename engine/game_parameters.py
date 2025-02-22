from dataclasses import dataclass

from engine.placement_rule import PlacementRule

@dataclass
class GameParameters:
    rows: int
    cols: int
    win_count: int
    placement_rule: PlacementRule
