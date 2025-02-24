import re
import string

from game.dim import within_bounds
from game.exceptions import CellBoundsException, IllegalMove
from game.move import Move
from game.placement_rule import PlacementRule
from game.piece import Piece
from game.typedefs import BoardSize, Cell

RE_MOVE_CELL = re.compile(r'([a-zA-Z])(\d)')

class Board:
    """
    Implements an abstract m,n,k-game like tic-tac-toe or Connect Four.

    By abstract, it's meant that notions like pieces falling due to gravity,
    like in Connect Four for example, aren't considered. To put it another
    way, the game can be imagined being played horizontally and pieces are
    placed anywhere where the player commands.

    Of course, the rules of the game are still respected so if a user places a
    piece in the middle of a Connect Four board, for example, an IllegalMove
    exception will be generated to ensure the integrity of the game.
    """

    def __init__(self,
                 size: BoardSize = (3, 3),
                 win_count: int = 3,
                 placement_rule: PlacementRule = PlacementRule.ANYWHERE) -> None:
        """
        :param size: (rows, cols) of board
        :param win: number in a row it takes to win
        :param placement_rule: constraint on where pieces can be placed
        """
        # Avoid circular import since WinDetector depends on having a Board
        from game.win_detector import WinDetector

        self.size: BoardSize = size
        self.win_count: int = win_count
        self.placement_rule: PlacementRule = placement_rule
        self.win_detector = WinDetector(self)
        self.reset()

    def reset(self) -> None:
        self._remove_pieces_from_board()
        self.win_detector.reset()

    def _remove_pieces_from_board(self) -> None:
        rows, cols = self.size
        tbl = []
        for _ in range(rows):
            row = [Piece._ for _ in range(cols)]
            tbl.append(row)
        self.tbl = tbl

    def full(self) -> bool:
        """Return True if the board is full of pieces"""
        for row in self.tbl:
            for piece in row:
                if piece == Piece._:
                    return False
        return True

    def win(self) -> bool:
        """Return True if a winning sequence is present"""
        return self.win_detector.win()

    @classmethod
    def cell_in_bounds(self, cell: Cell, sz: BoardSize) -> bool:
        """Returns True if the cell is within the bounds of the board"""
        coords = list(cell)
        upper_bounds = list(sz)
        lower_bounds = [0 for _ in upper_bounds]
        return within_bounds(coords, lower_bounds, upper_bounds)

    def pretty(self, coords=False) -> str:
        """
        :param coords: if True, include coordinate headings
        """
        _, cols = self.size

        # If we have coordinates enabled then things will be shifted to the
        # right by the coordinates on the left side
        horiz_shift = 2 if coords else 0
        horiz_blank = " " * horiz_shift

        vert_break = "|"
        blank_vert = " " * len(vert_break)

        cell_width = 3
       
        horiz_line_width = cell_width * cols
        horiz_line_width += len(vert_break) * (cols - 1)
        horiz_line = horiz_blank + ("-" * horiz_line_width)

        pretty_tbl = []

        if coords:
            low = string.ascii_lowercase
            row_heading = [
                low[i].center(cell_width) for i in range(cols)]
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

    def top_empty_row_for_column(self, col: int) -> int:
        """Return the row for the 'top' empty cell in a column

        Returns 0 if there are no empty cells in column
        """
        rows, _ = self.size
        last_row_idx = rows - 1
        for row in range(last_row_idx, 0, -1):
            piece = self.tbl[row][col]
            if piece == Piece._:
                return row

        return 0 

    def _check_column_stack(self, m: Move) -> None:
        row = self.top_empty_row_for_column(m.col)
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

        if not Board.cell_in_bounds(m.cell, self.size):
            raise CellBoundsException(f"cell out of bounds ({m=} {b=})")

        r = self.tbl[m.row]

        if r[m.col] != Piece._:
            raise IllegalMove(f"cell already occupied by piece ({m=})")

        self._check_piece_placement_rule(m)

        r[m.col] = m.piece

    def _parse_column_letter(self, col_letter: str) -> int:
        """Returns index associated with a given column letter

        For example, 'a' return 0, 'b' returns 1, etc...
        """
        col_letter = col_letter.lower()
        if len(col_letter) != 1:
            raise ValueError(f"column must be a single letter ({col_letter})")
        if col_letter not in string.ascii_lowercase:
            raise ValueError(
                f"column must be specified as a letter ({col_letter})")

        col = ord(col_letter) - ord('a')

        _, cols = self.size
        on_board = (0 <= col < cols)
        if not on_board:
            raise CellBoundsException(f"cell out of bounds {col_letter=}")

        return col

    def _parse_cell(self, token: str) -> Cell:
        """Token is like 'a1'"""
        match = RE_MOVE_CELL.match(token)
        if not match:
            raise ValueError(f"syntax error in move coordinate {token=}")

        col_letter, row_num_str = match.groups()

        col_idx = self._parse_column_letter(col_letter)

        try:
            row_num = int(row_num_str)
        except ValueError:
            raise ValueError(f"row number must be a number {token=}")

        row_idx = row_num - 1

        cell = (row_idx, col_idx)

        if not Board.cell_in_bounds(cell, self.size):
            raise CellBoundsException(f"cell out of bounds {token=}")

        return cell

    def parse_piece_placement(self, token: str) -> Cell:
        """
        A placement is a token which describes where to place a piece on the board.

        For games like tic-tac-toe where the placement rule is ANYWHERE, the
        placement must be a coordinate, like 'a1'.

        For games like Connect Four where the placement rule is COLUMN_STACK,
        then only a column letter is necessary. Coordinates are also allowed in
        these cases as well.
        """
        if self.placement_rule == PlacementRule.COLUMN_STACK and len(token) == 1:
            col = self._parse_column_letter(token)

            # This simulates gravity by placing the piece on the first not empty row
            # in that column
            row = self.top_empty_row_for_column(col)
            return (row, col)

        return self._parse_cell(token)