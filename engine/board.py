import string

from engine.exceptions import IllegalMove
from engine.enums import Piece
from engine.move import Move
from engine.typedefs import StateTable

class Board:
    """
    Implements a m,n,k-game
    """

    def __init__(self, rows: int = 3, cols: int = 3,
                 win_count: int = 3) -> None:
        """
        :param win: number in a row it takes to win
        """
        self.rows: int = rows
        self.cols: int = cols
        self.win_count: int = win_count
        self.tbl: StateTable = self._init_tbl(rows, cols)

    def _init_tbl(self, rows: int, cols: int) -> StateTable:
        tbl = []
        for _ in range(rows):
            row = [Piece._ for _ in range(cols)]
            tbl.append(row)
        return tbl

    def full(self) -> bool:
        """Return True if the board is full of pieces"""
        for row in self.tbl:
            for piece in row:
                if piece == Piece._:
                    return False
        return True

    def win(self) -> bool:
        """Return True if a winning sequence is present"""
        # - direction
        for row_idx in range(self.rows):
            row_seq = self.tbl[row_idx]
            if self._winning_sequence(row_seq):
                return True

        # | direction
        for col_idx in range(self.cols):
            col_seq = [row[col_idx] for row in self.tbl]
            if self._winning_sequence(col_seq):
                return True

        # / direction
        slash_seq = [row[self.cols - idx - 1] for idx, row in enumerate(self.tbl)]
        if self._winning_sequence(slash_seq):
            return True

        # \ direction
        backslash_seq = [row[idx] for idx, row in enumerate(self.tbl)]
        if self._winning_sequence(backslash_seq):
            return True

        return False

    def _winning_sequence(self, piece_seq: list[Piece]) -> bool:
        """Returns True if a list of pieces (corresponding to rows, cols, or
        diagonals) are a winning sequence: we have `win_count` in a row
        """
        prev_piece = None
        run_count = 0

        for piece in piece_seq:
            if piece == Piece._:
                run_count = 0
            elif prev_piece is None:
                run_count = 1
            elif prev_piece != piece:
                run_count = 1
            elif prev_piece == piece:
                run_count += 1

            if run_count >= self.win_count:
                return True

            prev_piece = piece

        return False

    def pretty(self, coords=False) -> str:
        """
        :param coords: if True, include coordinate headings
        """
        # If we have coordinates enabled then things will be shifte to the
        # right by the coordinates on the left side
        horiz_shift = 2 if coords else 0
        horiz_blank = " " * horiz_shift

        vert_break = "|"
        blank_vert = " " * len(vert_break)

        cell_width = 3
       
        horiz_line_width = cell_width * self.cols
        horiz_line_width += len(vert_break) * (self.cols - 1)
        horiz_line = horiz_blank + ("-" * horiz_line_width)

        pretty_tbl = []

        if coords:
            low = string.ascii_lowercase
            row_heading = [
                low[i].center(cell_width) for i in range(self.cols)]
            row_heading_str = horiz_blank + blank_vert.join(row_heading)

            pretty_tbl.append(row_heading_str)

        for idx, row in enumerate(self.tbl):
            pretty_row = []
            for piece in row:
                piece_str = piece.pretty().center(cell_width)
                pretty_row.append(piece_str)

            pretty_row_str = vert_break.join(pretty_row)

            if coords:
                row_coord = idx + 1
                row_coord_str = str(row_coord).ljust(horiz_shift)
                pretty_row_str = f"{row_coord_str}{pretty_row_str}"

            pretty_tbl.append(pretty_row_str)

            last_row = idx == len(self.tbl) - 1
            if not last_row:
                pretty_tbl.append(horiz_line)

        pretty_tbl_str = "\n".join(pretty_tbl)
        return pretty_tbl_str

    def apply_move(self, m: Move) -> None:
        if m.piece == Piece._:
            raise IllegalMove(f"piece cannot be blank ({m=})")

        b = self

        if m.row > self.rows - 1:
            raise IllegalMove(f"move row out of bounds ({m=} {b=})")
        if m.col > self.cols - 1:
            raise IllegalMove(f"move col out of bounds ({m=} {b=})")

        r = self.tbl[m.row]

        if r[m.col] != Piece._:
            raise IllegalMove(f"cell already occupied by piece ({m=})")

        r[m.col] = m.piece
