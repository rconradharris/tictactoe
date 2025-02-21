from enum import Enum

class Player(Enum):
    P1 = 1
    P2 = 2


class Mark(Enum):
    _ = 0
    X = 1
    O = 2  # noqa: E741 (typographically ambiguous with zero, but thats okay)

    def pretty(self) -> str:
        if self == self._:
            return "_"
        elif self == self.X:
            return "X"
        elif self == self.O:
            return "O"

        return "?"

    @classmethod
    def from_str(cls, s: str) -> 'Mark':
        if s == "_":
            return cls._
        elif s == "X":
            return cls.X
        elif s == "O":
            return cls.O

        raise ValueError(f"unknown mark: '{s}'")


class GameState(Enum):
    INIT = 0 
    PLAYING = 1 
    WON = 2
    CAT_GAME = 3


