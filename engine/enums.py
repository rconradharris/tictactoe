from enum import Enum, auto
from typing import Tuple


class Player(Enum):
    P1 = auto()
    P2 = auto()


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


class Piece(Enum):
    _ = auto() 
    X = auto()
    O = auto()  # noqa: E741 (typographically ambiguous with zero, but thats okay)

    def pretty(self) -> str:
        if self == self._:
            return "_"
        elif self == self.X:
            return "X"
        elif self == self.O:
            return "O"

        return "?"

    @classmethod
    def from_str(cls, s: str) -> 'Piece':
        if s == "_":
            return cls._
        elif s == "X":
            return cls.X
        elif s == "O":
            return cls.O

        raise ValueError(f"unknown piece: '{s}'")

    def next(self) -> 'Piece':
        """Returns the next piece in the sequence, i.e. X -> O"""
        if self == Piece.X:
            return Piece.O
        elif self == Piece.O:
            return Piece.X

        raise Exception("only X and O pieces are sequencable")


class GameState(Enum):
    INIT = auto() 
    PLAYING = auto() 
    FINISHED = auto()


class Direction(Enum):
    # |
    N_S = auto()
    S_N = auto()

    # -
    W_E = auto()
    E_W = auto()

    # /
    SW_NE = auto()
    NE_SW = auto()

    # \
    NW_SE = auto()
    SE_NW = auto()

    def transform(self) -> Tuple[int, int]:
        """Returns the tuple that describes how to modify a given cell
        coordinate to translate in the given direction. The tuple is of form
        (row_delta, col_delta)
        """
        if self == Direction.N_S:
            return (1, 0)
        elif self == Direction.S_N:
            return (-1, 0)
        elif self == Direction.W_E:
            return (0, 1)
        elif self == Direction.E_W:
            return (0, -1)
        elif self == Direction.SW_NE:
            return (-1, 1)
        elif self == Direction.NE_SW:
            return (1, -1)
        elif self == Direction.NW_SE:
            return (1, 1)
        elif self == Direction.SE_NW:
            return (-1, -1)
        else:
            raise ValueError(f"unknown direction {self}")
