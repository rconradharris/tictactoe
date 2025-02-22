from enum import Enum, auto


class PlacementRule(Enum):
    # Tic-tac-toe like
    ANYWHERE = auto()

    # Connect Four-like
    COLUMN_STACK = auto()

    @classmethod
    def from_str(cls, s: str) -> 'PlacementRule':
        x = s.lower()
        if x == "anywhere":
            return cls.ANYWHERE
        elif x == "columnstack":
            return cls.COLUMN_STACK

        raise ValueError(f"unknown piece placement rule: '{s}'")
