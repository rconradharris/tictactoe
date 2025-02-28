from enum import Enum, auto


class FirstMove(Enum):
    COIN_TOSS = auto()
    HUMAN = auto()
    ENGINE = auto()

    @classmethod
    def all(cls) -> list["FirstMove"]:
        return [
            cls.COIN_TOSS,
            cls.HUMAN,
            cls.ENGINE,
        ]

    def pretty(self) -> str:
        if self == FirstMove.COIN_TOSS:
            return "cointoss"
        elif self == FirstMove.HUMAN:
            return "human"
        elif self == FirstMove.ENGINE:
            return "engine"
        return "?"

    @classmethod
    def from_str(cls, s: str) -> "FirstMove":
        if s == "cointoss":
            return cls.COIN_TOSS
        elif s == "human":
            return cls.HUMAN
        elif s == "engine":
            return cls.ENGINE
        else:
            raise ValueError("unknown first move")
