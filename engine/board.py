import re
import string
from typing import Generator

from engine.exceptions import IllegalMove
from engine.enums import Piece
from engine.move import Move
from engine.placement_rule import PlacementRule
from engine.typedefs import Cell, StateTable

RE_MOVE_COORD = re.compile(r'([a-zA-Z])(\d)')

class Board:
    """
    Implements a m,n,k-game
    """

    def __init__(self,
                 rows: int = 3,
                 cols: int = 3,
                 win_count: int = 3,
                 placement_rule: PlacementRule = PlacementRule.ANYWHERE) -> None:
        """
        :param rows: number of rows tall the grid is
        :param cols: number of columns wide the grid is
        :param win: number in a row it takes to win
        :param placement_rule: constraint on where pieces can be placed
        """
        self.rows: int = rows
        self.cols: int = cols
        self.win_count: int = win_count
        self.placement_rule: PlacementRule = placement_rule

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
        if self._row_win():
            return True

        # | direction
        if self._col_win():
            return True

        # / direction
        if self._slash_win():
            return True

        # \ direction
        if self._backslash_win():
            return True

        return False

    def _cell_in_bounds(self, cell: Cell) -> bool:
        """Returns True if the cell is within the bounds of the board"""
        row, col = cell
        return (0 <= row < self.rows) and (0 <= col < self.cols)

    def _cell_sequence(self, cell, row_delta: int, col_delta: int) -> Generator[Cell]:
        """Yield cells in a direction specified by row_delta and col_delta"""
        row, col = cell

        while True:
            if not self._cell_in_bounds((row, col)):
                return

            yield (row, col)

            row += row_delta
            col += col_delta

    def _row_cells(self, cell) -> Generator[Cell]:
        """Yield cells in the - direction starting at (row, col)

        Row direction fixes row and increments column.
        """
        for cell in self._cell_sequence(cell, row_delta=0, col_delta=1):
            yield cell

    def _col_cells(self, cell) -> Generator[Cell]:
        """Yield cells in the | direction starting at (row, col)

        Row direction increments row and fixes column.
        """
        for cell in self._cell_sequence(cell, row_delta=1, col_delta=0):
            yield cell

    def _slash_cells(self, cell) -> Generator[Cell]:
        """Yield cells in the / direction starting at (row, col)

        Slashes decrement row and increment column.
        """
        for cell in self._cell_sequence(cell, row_delta=-1, col_delta=1):
            yield cell

    def _backslash_cells(self, cell) -> Generator[Cell]:
        """Yield cells in the backslash direction starting at (row, col)

        Backslashes increment row and increment column.
        """
        for cell in self._cell_sequence(cell, row_delta=1, col_delta=1):
            yield cell

    def _row_win(self) -> bool:
        for ref_row in range(self.rows):
            seq = []
            for row, col in self._row_cells((ref_row, 0)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
                return True

        return False

    def _col_win(self) -> bool:
        for ref_col in range(self.cols):
            seq = []
            for row, col in self._col_cells((0, ref_col)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
                return True

        return False

    def _slash_win(self) -> bool:
        # / down the rows
        for ref_row in range(self.rows):
            seq = []
            for row, col in self._slash_cells((ref_row, 0)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
                return True

        # / across the columns of last row, start at 1 since we already did 0
        # above
        last_row_idx = self.rows - 1
        for ref_col in range(1, self.cols):
            seq = []
            for row, col in self._slash_cells((last_row_idx, ref_col)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
                return True

        return False

    def _backslash_win(self) -> bool:
        # \ down the rows
        for ref_row in range(self.rows):
            seq = []
            for row, col in self._backslash_cells((ref_row, 0)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
                return True

        # \ across the columns of first row, start at 1 since we already did 0
        # above
        for ref_col in range(1, self.cols):
            seq = []
            for row, col in self._backslash_cells((0, ref_col)):
                #print(f"{row=} {col=}")
                piece = self.tbl[row][col]
                seq.append(piece)

            #print(f"{seq=}")
            if self._winning_sequence(seq):
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

    def _top_empty_row_for_column(self, col: int) -> int:
        """Return the row for the 'top' empty cell in a column

        Returns 0 if there are no empty cells in column
        """
        last_row_idx = self.rows - 1
        for row in range(last_row_idx, 0, -1):
            piece = self.tbl[row][col]
            if piece == Piece._:
                return row

        return 0 

    def _check_column_stack(self, m: Move) -> None:
        row = self._top_empty_row_for_column(m.col)
        if m.row != row:
            raise IllegalMove(f"move must stack ({m=})")

    def _check_piece_placement_rule(self, m: Move) -> None:
        if self.placement_rule == PlacementRule.ANYWHERE:
            return

        if self.placement_rule == PlacementRule.COLUMN_STACK:
            self._check_column_stack(m)
            return

    def apply_move(self, m: Move) -> None:
        if m.piece == Piece._:
            raise IllegalMove(f"piece cannot be blank ({m=})")

        b = self

        if not self._cell_in_bounds((m.row, m.col)):
            raise IllegalMove(f"cell out of bounds ({m=} {b=})")

        r = self.tbl[m.row]

        if r[m.col] != Piece._:
            raise IllegalMove(f"cell already occupied by piece ({m=})")

        self._check_piece_placement_rule(m)

        r[m.col] = m.piece

    @classmethod
    def parse_algebraic_cell(cls, token: str) -> Cell:
        """Token is like 'a1' """
        match = RE_MOVE_COORD.match(token)
        if not match:
            raise ValueError(f"syntax error in move coordinate {token=}")

        col_letter, row_num_str = match.groups()

        col_letter = col_letter.lower()

        col_idx = ord(col_letter) - ord('a')

        try:
            row_num = int(row_num_str)
        except ValueError:
            raise ValueError(f"row number must be a number {token=}")

        row_idx = row_num - 1

        return (row_idx, col_idx)
