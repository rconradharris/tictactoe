import string

from game.exceptions import IllegalMove
from game.piece import Piece
from game.typedefs import Cell


class Move:
    cell: Cell
    piece: Piece

    def __init__(self, cell: Cell, piece: Piece):
        if cell[0] < 0:
            raise IllegalMove("row cannot be negative")
        if cell[1] < 0:
            raise IllegalMove("col cannot be negative")

        self.cell = cell
        self.piece = piece

    @property
    def row(self) -> int:
        return self.cell[0]

    @property
    def col(self) -> int:
        return self.cell[1]

    @property
    def col_letter(self) -> str:
        return string.ascii_lowercase[self.col]

    def pretty(self) -> str:
        p_str = self.piece.pretty()
        return f"{self.col_letter}{self.row+1}:{p_str}"

    def __repr__(self) -> str:
        """Provide a more concise repr than dataclass default"""
        return self.pretty()


NULL_MOVE = Move((0, 0), Piece._)
