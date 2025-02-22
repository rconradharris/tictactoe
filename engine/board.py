import string

from engine.exceptions import IllegalMove
from engine.enums import Mark
from engine.move import Move
from engine.typedefs import StateTable

class Board:

    def __init__(self, rows: int = 3, cols: int = 3):
        if rows != cols:
            raise ValueError(f"board must be square ({rows=} {cols=})")

        self.rows: int = rows
        self.cols: int = cols
        self.tbl: StateTable = self._init_tbl(rows, cols)

    def _init_tbl(self, rows: int, cols: int) -> StateTable:
        tbl = []
        for _ in range(rows):
            row = [Mark._ for _ in range(cols)]
            tbl.append(row)
        return tbl

    def full(self) -> bool:
        """Return True if the board is full of marks"""
        for row in self.tbl:
            for mark in row:
                if mark == Mark._:
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

    def _winning_sequence(self, mark_seq: list[Mark]) -> bool:
        """Returns True if a list of marks (corresponding to rows, cols, or
        diagonals) are a winning sequence: all the same, not blanks
        """
        prev_mark = None

        for mark in mark_seq:
            if mark == Mark._:
                return False

            if prev_mark is not None and prev_mark != mark:
                # Found a different mark, no winner here
                return False

            prev_mark = mark

        # All marks the same, chicken dinner
        return True


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
            for mark in row:
                mark_str = mark.pretty().center(cell_width)
                pretty_row.append(mark_str)

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
        if m.mark == Mark._:
            raise IllegalMove(f"mark cannot be blank ({m=})")

        b = self

        if m.row > self.rows - 1:
            raise IllegalMove(f"move row out of bounds ({m=} {b=})")
        if m.col > self.cols - 1:
            raise IllegalMove(f"move col out of bounds ({m=} {b=})")

        r = self.tbl[m.row]

        if r[m.col] != Mark._:
            raise IllegalMove(f"spot already marked ({m=})")

        r[m.col] = m.mark
