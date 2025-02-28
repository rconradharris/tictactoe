from enum import Enum, auto


class Command(Enum):
    """These are special commands you can use from the prompt."""

    SHOW_BOARD = auto()
    HELP = auto()

    @classmethod
    def from_str(cls, s: str) -> "Command":
        if s == ".":
            return cls.SHOW_BOARD
        elif s == "?":
            return cls.HELP
        else:
            raise ValueError(f"unknown command: '{s}'")
