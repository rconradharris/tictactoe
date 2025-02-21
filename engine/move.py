from engine.enums import Mark
from engine.exceptions import IllegalMove

class Move:
    row: int
    col: int
    mark: Mark

    def __init__(self, row: int, col: int, mark: Mark):
        if row < 0:
            raise IllegalMove("row cannot be negative")
        self.row = row

        if col < 0:
            raise IllegalMove("col cannot be negative")
        self.col = col
        self.mark = mark

    def __repr__(self):
        """Provide a more concise repr than dataclass default"""
        return f"Move({self.row}, {self.col}, {self.mark.pretty()})"
