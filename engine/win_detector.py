from typing import Generator

from engine.board import Board
from engine.enums import Direction, Piece
from engine.typedefs import BoardSize, Cell


class WinDetector:
    """
    This class is repsonsible for detecting if a player has won the game.

    This involves scanning in various directions according to the
    dimensionality of the board. For a 2D board, we scan horizontal, vertical,
    forward slash diagonally and backslash diagonally.
    """
    def __init__(self, board: Board) -> None:
        self.board = board
        self.seq_detector = PieceSequenceDetector(board)

    @property
    def rows(self) -> int:
        rows, _, = self.board.size
        return rows

    @property
    def cols(self) -> int:
        _, cols, = self.board.size
        return cols

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

    def _cell_sequence(self, cell: Cell, row_delta: int, col_delta: int) -> Generator[Cell]:
        """Yield cells in a direction specified by row_delta and col_delta"""
        row, col = cell
        sz = (self.rows, self.cols)

        while True:
            if not Board.cell_in_bounds((row, col), sz):
                return

            yield (row, col)

            row += row_delta
            col += col_delta

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
        sz = (self.board.rows, self.board.cols)
        origin = (0, 0)

        for r1, c1 in _directional_scan(origin, Direction.N_S, sz):
            self.seq_detector.reset()

            for r2, c2 in _directional_scan((r1, 0), Direction.W_E, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True

        return False

    def _col_win(self) -> bool:
        sz = (self.board.rows, self.board.cols)
        origin = (0, 0)

        for r1, c1 in _directional_scan(origin, Direction.W_E, sz):
            self.seq_detector.reset()

            for r2, c2 in _directional_scan((0, c1), Direction.N_S, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True

        return False

    def _slash_win(self) -> bool:
        # / down the rows
        for ref_row in range(self.rows):
            seq = []
            for row, col in self._slash_cells((ref_row, 0)):
                #print(f"{row=} {col=}")
                piece = self.board.tbl[row][col]
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
                piece = self.board.tbl[row][col]
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
                piece = self.board.tbl[row][col]
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
                piece = self.board.tbl[row][col]
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

            if run_count >= self.board.win_count:
                return True

            prev_piece = piece

        return False


class PieceSequenceDetector:
    """Class for detecting if a sequence of k pieces are seen in a row
    """
    def __init__(self, board: Board) -> None:
        self.board = board
        self.reset()

    def reset(self) -> None:
        self.prev_piece: Piece | None = None
        self.run_count: int = 0

    def put(self, piece: Piece) -> bool:
        """Returns True if the latest piece caused a win, otherwise False
        """
        if piece == Piece._:
            self.run_count = 0
        elif self.prev_piece is None:
            self.run_count = 1
        elif self.prev_piece != piece:
            self.run_count = 1
        elif self.prev_piece == piece:
            self.run_count += 1

        if self.run_count >= self.board.win_count:
            return True

        self.prev_piece = piece
        return False


def _directional_scan(origin: Cell,
                      dir_: Direction,
                      sz: BoardSize) -> Generator[Cell]:
    """Scan cells starting at origin in the given direction until board
    boundary is hit
    """
    row, col = origin
    row_delta, col_delta = dir_.transform()

    while True:
        cell = (row, col)

        if not Board.cell_in_bounds(cell, sz):
            return

        yield cell

        row += row_delta
        col += col_delta
