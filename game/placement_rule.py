from enum import Enum, auto


class PlacementRule(Enum):
    """
    A PlacementRule encapulates any restriction on how a player may place a
    Piece on the Board.

    For example, in tic-tac-toe a player can place a piece anywhere save for
    the trivial case of a cell already being occupied.

    In Connect Four, however, a piece must be placed at the lowest unoccupied
    cell in a column, which simulates gravity pulling the piece down. This is
    called a "column stack".
    """

    # Tic-tac-toe like
    ANYWHERE = auto()

    # Connect Four-like
    COLUMN_STACK = auto()

    @classmethod
    def from_str(cls, s: str) -> "PlacementRule":
        x = s.lower()
        if x == "anywhere":
            return cls.ANYWHERE
        elif x == "columnstack":
            return cls.COLUMN_STACK

        raise ValueError(f"unknown piece placement rule: '{s}'")
