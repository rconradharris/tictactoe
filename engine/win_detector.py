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
        sz = (self.board.rows, self.board.cols)
        origin = (0, 0)

        # Scan | down
        for r1, c1 in _directional_scan(origin, Direction.N_S, sz):
            self.seq_detector.reset()

            # Scan / up
            for r2, c2 in _directional_scan((r1, 0), Direction.SW_NE, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True


        # Scan - right
        last_row_idx = self.board.rows - 1
        for r1, c1 in _directional_scan((last_row_idx, 1), Direction.W_E, sz):
            self.seq_detector.reset()

            # Scan / up from last row, start at col 1 since we already did col 0
            # in the previous pass
            for r2, c2 in _directional_scan((r1, c1), Direction.SW_NE, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True

        return False

    def _backslash_win(self) -> bool:
        sz = (self.board.rows, self.board.cols)
        origin = (0, 0)

        # Scan | down
        for r1, c1 in _directional_scan(origin, Direction.N_S, sz):
            self.seq_detector.reset()

            # Scan \ down
            for r2, c2 in _directional_scan((r1, 0), Direction.NW_SE, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True


        # Scan - right on first row, start at col 1 since we already did col 0
        # in the previous pass
        for r1, c1 in _directional_scan((0, 1), Direction.W_E, sz):
            self.seq_detector.reset()

            for r2, c2 in _directional_scan((r1, c1), Direction.SW_NE, sz):
                piece = self.board.tbl[r2][c2]

                if self.seq_detector.put(piece):
                    return True

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
