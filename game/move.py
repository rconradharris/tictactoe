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

    def __repr__(self) -> str:
        """Provide a more concise repr than dataclass default"""
        row, col = self.cell
        return f"Move({row}, {col}, {self.piece.pretty()})"
