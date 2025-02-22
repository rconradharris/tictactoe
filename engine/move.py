from engine.enums import Piece
from engine.exceptions import IllegalMove

class Move:
    row: int
    col: int
    piece: Piece

    def __init__(self, row: int, col: int, piece: Piece):
        if row < 0:
            raise IllegalMove("row cannot be negative")
        self.row = row

        if col < 0:
            raise IllegalMove("col cannot be negative")
        self.col = col
        self.piece = piece

    def __repr__(self) -> str:
        """Provide a more concise repr than dataclass default"""
        return f"Move({self.row}, {self.col}, {self.piece.pretty()})"
