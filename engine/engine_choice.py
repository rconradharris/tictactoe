from enum import Enum, auto

from engine.engine import Engine


class EngineChoice(Enum):
    DUMMY = auto()
    RANDIMAXER = auto()
    WINIMAXER = auto()
    WINIBETAMAXER = auto()

    def engine(self) -> type[Engine]:
        if self == EngineChoice.DUMMY:
            from engine.mnk.dummy import Dummy

            return Dummy
        elif self == EngineChoice.RANDIMAXER:
            from engine.mnk.randimaxer import Randimaxer

            return Randimaxer
        elif self == EngineChoice.WINIMAXER:
            from engine.mnk.winimaxer import Winimaxer

            return Winimaxer
        elif self == EngineChoice.WINIBETAMAXER:
            from engine.mnk.winibetamaxer import Winibetamaxer

            return Winibetamaxer

        raise ValueError("unknown engine choice")

    def pretty(self) -> str:
        if self == EngineChoice.DUMMY:
            return "dummy"
        elif self == EngineChoice.RANDIMAXER:
            return "randimaxer"
        elif self == EngineChoice.WINIMAXER:
            return "winimaxer"
        elif self == EngineChoice.WINIBETAMAXER:
            return "winibetamaxer"

    @classmethod
    def from_str(cls, s: str) -> "EngineChoice":
        if s == "dummy":
            return cls.DUMMY
        elif s == "randimaxer":
            return cls.RANDIMAXER
        elif s == "winimaxer":
            return cls.WINIMAXER
        elif s == "winibetamaxer":
            return cls.WINIBETAMAXER

        raise ValueError(f"unknown engine choice: {s}")
