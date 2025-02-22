from enum import Enum, auto

from at3.exceptions import UnknownFieldException


class ParseState(Enum):
    INIT = auto()
    METADATA = auto()
    METADATA_DONE = auto()
    MOVE_NUMBER = auto()
    MOVE_CELL = auto()
    DONE = auto()


class KnownField(Enum):
    """These are fields defined by the spec. Other fields can be included, but
    they'll just be treated as arbitrary strings
    """
    EVENT = auto()
    SITE = auto()
    DATE = auto()
    PLAYER1 = auto()
    PLAYER2 = auto()
    RESULT = auto()
    PLAYER1_ELO = auto()
    PLAYER2_ELO = auto()
    TIME_CONTROL = auto()
    PLACEMENT_RULE = auto()
    GRID = auto()
    WIN_COUNT = auto()
    GAME_CHOICE = auto()
    PLAYER1_CHOICE = auto()

    @classmethod
    def from_str(cls, field_name: str) -> 'KnownField':
        s = field_name.lower()

        if s == "event":
            return cls.EVENT
        elif s == "site":
            return cls.SITE
        elif s == "date":
            return cls.DATE
        elif s == "player1":
            return cls.PLAYER1
        elif s == "player2":
            return cls.PLAYER2
        elif s == "result":
            return cls.RESULT
        elif s == "player1elo":
            return cls.PLAYER1_ELO
        elif s == "player2elo":
            return cls.PLAYER2_ELO
        elif s == "timecontrol":
            return cls.TIME_CONTROL
        elif s == "placementrule":
            return cls.PLACEMENT_RULE
        elif s == "grid":
            return cls.GRID
        elif s == "wincount":
            return cls.WIN_COUNT
        elif s == "game":
            return cls.GAME_CHOICE
        elif s == "player1choice":
            return cls.PLAYER1_CHOICE

        raise UnknownFieldException(
                f"unknown field: '{field_name}'")
