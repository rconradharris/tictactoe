from enum import Enum, auto

from game.game_parameters import GameParameters
from game.placement_rule import PlacementRule


class GameChoice(Enum):
    """Acts as a fixed menu for certain game parameters so you don't have to
    fill in Grid, WinCount and PlacementRule explicitly.
    """
    UNDEFINED = auto()
    TIC_TAC_TOE = auto()
    CONNECT_FOUR = auto()

    @classmethod
    def from_str(cls, choice: str) -> 'GameChoice':
        s = choice.lower()

        if s == "undefined":
            return cls.UNDEFINED
        elif s == "tictactoe":
            return cls.TIC_TAC_TOE
        elif s == "connectfour":
            return cls.CONNECT_FOUR

        raise ValueError(f"unknown game choice: '{choice}'")

    @classmethod
    def from_abbrev(cls, abbrev: str) -> 'GameChoice':
        s = abbrev.lower()

        if s == "undefined":
            return cls.UNDEFINED
        elif s == "t3":
            return cls.TIC_TAC_TOE
        elif s == "c4":
            return cls.CONNECT_FOUR

        raise ValueError(f"unknown game choice abbreviation: '{abbrev}'")

    def parameters(self) -> GameParameters | None:
        """Returns game parameters for given GameChoice.

        Return None if no parameters are associated with choice.
        """
        if self == GameChoice.TIC_TAC_TOE:
            return GameParameters(
                size = (3, 3),
                win_count=3,
                placement_rule=PlacementRule.ANYWHERE
            )
        elif self == GameChoice.CONNECT_FOUR:
            return GameParameters(
                size = (6, 7),
                win_count=4,
                placement_rule=PlacementRule.COLUMN_STACK
            )

        return None
