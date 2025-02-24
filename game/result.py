
from enum import Enum, auto


class Result(Enum):
    UNDEFINED = auto()
    UNFINISHED = auto()
    PLAYER1_VICTORY = auto()
    PLAYER2_VICTORY = auto()
    DRAW = auto()

    def pretty(self) -> str:
        if self == self.UNDEFINED:
            return "Undefined"
        elif self == self.UNFINISHED:
            return "Unfinished"
        elif self == self.PLAYER1_VICTORY:
            return "1-0"
        elif self == self.PLAYER2_VICTORY:
            return "0-1"
        elif self == self.DRAW:
            return "1/2-1/2"

        return "?"

    @classmethod
    def from_str(cls, s: str) -> 'Result':
        s = s.lower()

        if s == "undefined":
            return cls.UNDEFINED
        elif s == "unfinished":
            return cls.UNFINISHED
        elif s == "1-0":
            return cls.PLAYER1_VICTORY
        elif s == "0-1":
            return cls.PLAYER2_VICTORY
        elif s == "1/2-1/2":
            return cls.DRAW

        raise ValueError(f"unknown result: '{s}'")