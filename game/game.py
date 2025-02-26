from enum import Enum, auto
from typing import Generator

from game.board import Board
from game.exceptions import (
    IllegalMove,
    PieceSelectionsAlreadyMade,
    PieceSelectionException,
    InvalidPieceSelection,
)
from game.move import Move
from game.player import Player
from game.piece import Piece
from game.result import Result


class GameState(Enum):
    INIT = auto() 
    PIECES_CHOSEN = auto()
    PLAYING = auto() 
    FINISHED = auto()


class Game:
    """
    Game ends in the FINISHED state with a result set.
    """

    def __init__(self, board: Board):
        self.board: Board = board
        self.reset()

    def reset(self) -> None:
        self.cur_player: Player = Player.P1
        self._player2piece: dict[Player, Piece] = {}
        self._piece2player: dict[Piece, Player] = {}
        self.state: GameState = GameState.INIT
        self.result: Result = Result.UNFINISHED
        self.move_history: list[Move] = []
        self.board.reset()

    @property
    def move_num(self) -> int:
        """Return the current move number (starting from 1)"""
        return len(self.move_history) + 1

    @property
    def cur_piece(self) -> Piece:
        """Return Piece associated with the current player on-move"""
        return self._player2piece[self.cur_player]

    def _end_turn(self) -> None:
        if self.cur_player == Player.P1:
            self.cur_player = Player.P2
        else:
            self.cur_player = Player.P1

    def _check_piece_consistency(self, m: Move) -> None:
        """Ensure players cannot switch pieces once they've chosen"""
        p = m.piece
        if p == Piece._:
            raise IllegalMove(f"piece cannot be blank ({m=})")
        elif p != self.cur_piece:
            raise IllegalMove(f"player cannot switch pieces ({m=})")

    def _check_game_state_pre_move(self, m: Move) -> None:
        if self.state == GameState.INIT:
            raise IllegalMove(f"cannot move until pieces chosen ({m=})")
        elif self.state == GameState.FINISHED:
            raise IllegalMove(f"cannot move after a game has finished ({m=})")

    def _start_game_if_needed(self) -> None:
        if self.state == GameState.PIECES_CHOSEN:
            self.state = GameState.PLAYING

    def _finish_game(self, r: Result) -> None:
        self.result = r
        self.state = GameState.FINISHED

    def _adjust_game_state_post_move(self) -> None:
        if self.board.win():

            if self.cur_player == Player.P1:
                self._finish_game(Result.PLAYER1_VICTORY)
            elif self.cur_player == Player.P2:
                self._finish_game(Result.PLAYER2_VICTORY)

        elif self.board.full():
            self._finish_game(Result.DRAW)

    def _map_player_to_piece(self, player: Player, piece: Piece) -> None:
        self._player2piece[player] = piece
        self._piece2player[piece] = player

    def choose_player1_piece(self, p: Piece) -> None:
        """Declare player1's piece selection.

        This makes it so that the piece no longer needs to be passed in
        explicitly: the game can infer the current piece based on whose turn
        it is.
        """
        if self.state != GameState.INIT:
            raise PieceSelectionException("game state must be INIT")

        if self._player2piece or self._piece2player:
            raise PieceSelectionsAlreadyMade

        if p == Piece._:
            raise InvalidPieceSelection
        elif p == Piece.X:
            self._map_player_to_piece(Player.P1, Piece.X)
            self._map_player_to_piece(Player.P2, Piece.O)
        elif p == Piece.O:
            self._map_player_to_piece(Player.P1, Piece.O)
            self._map_player_to_piece(Player.P2, Piece.X)
        else:
            raise InvalidPieceSelection

        self.state = GameState.PIECES_CHOSEN

    def apply_move(self, m: Move) -> None:
        self._check_game_state_pre_move(m)

        self._start_game_if_needed()
        
        self._check_piece_consistency(m)

        self.board.apply_move(m)

        self.move_history.append(m)

        self._adjust_game_state_post_move()

        if self.state == GameState.PLAYING:
            self._end_turn()

    def create_move(self, placement_location: str) -> Move:
        """Place the current players piece at the location described by
        the location.

        In Tic-Tac-Toe, location should be a cell coordinate.

        In Connect Four, the location can just be a column letter.
        """
        cell = self.board.parse_piece_placement(placement_location)
        return Move(cell, self.cur_piece)

    def possible_moves(self) -> Generator[Move]:
        """Generate all possible moves for the current player"""
        for cell in self.board.playable_cells():
            yield Move(cell, self.cur_piece)

    def copy(self) -> 'Game':
        """Make a full copy of a game"""
        g1 = self

        # Use a dummy board to initialize, we'll overwrite with a proper copy
        # of the Board object afterward. This keeps initialization semantics
        # clean
        g2 = Game(Board())

        g2.cur_player = g1.cur_player
        g2._player2piece = g1._player2piece.copy()
        g2._piece2player = g1._piece2player.copy()
        g2.state = g1.state
        g2.result = g1.result
        g2.move_history = g1.move_history.copy()
        g2.board = g1.board.copy()

        return g2
