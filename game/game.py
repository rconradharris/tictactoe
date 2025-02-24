from enum import Enum, auto

from game.board import Board
from game.exceptions import IllegalMove
from game.move import Move
from game.player import Player
from game.piece import Piece
from game.result import Result


class GameState(Enum):
    INIT = auto() 
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
        self.piece_selections: dict[Piece, Player] = {}
        self.state: GameState = GameState.INIT
        self.result: Result = Result.UNFINISHED
        self.move_history: list[Move] = []
        self.board.reset()

    def _end_turn(self) -> None:
        if self.cur_player == Player.P1:
            self.cur_player = Player.P2
        else:
            self.cur_player = Player.P1

    def _check_piece_consistency(self, m: Move) -> None:
        """Ensure players cannot switch pieces once they've chosen"""
        cur_piece = m.piece

        if cur_piece == Piece._:
            raise IllegalMove(f"piece cannot be blank ({m=})")

        prev_player = self.piece_selections.get(cur_piece, None)

        if prev_player is not None and prev_player != self.cur_player:
            raise IllegalMove(f"player cannot switch pieces ({m=})")

    def _choose_piece_for_cur_player(self, m: Piece) -> None:
        """Declare a piece choice for the current player"""
        self.piece_selections[m] = self.cur_player 

    def _check_game_state_pre_move(self, m: Move) -> None:
        if self.state == GameState.FINISHED:
            raise IllegalMove(f"cannot move after a game has finished ({m=})")

    def _start_game_if_needed(self) -> None:
        if self.state == GameState.INIT:
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

    def apply_move(self, m: Move) -> None:
        self._check_game_state_pre_move(m)

        self._start_game_if_needed()
        
        self._check_piece_consistency(m)
        self._choose_piece_for_cur_player(m.piece)

        self.board.apply_move(m)

        self.move_history.append(m)

        self._adjust_game_state_post_move()

        if self.state == GameState.PLAYING:
            self._end_turn()
