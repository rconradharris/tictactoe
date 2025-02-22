from engine.board import Board
from engine.enums import GameState, Mark, Player, Result
from engine.exceptions import IllegalMove
from engine.move import Move

class Game:
    """
    Game ends in the FINISHED state with a result set.
    """

    def __init__(self, board: Board):
        self.board: Board = board
        self.reset()

    def reset(self) -> None:
        self.cur_player: Player = Player.P1
        self.mark_selections: dict[Mark, Player] = {}
        self.state: GameState = GameState.INIT
        self.result: Result = Result.UNFINISHED
        self.move_history: list[Move] = []

    def _end_turn(self) -> None:
        if self.cur_player == Player.P1:
            self.cur_player = Player.P2
        else:
            self.cur_player = Player.P1

    def _check_mark_consistency(self, m: Move) -> None:
        """Ensure players cannot switch marks once they've chosen"""
        cur_mark = m.mark

        if cur_mark == Mark._:
            raise IllegalMove(f"mark cannot be blank ({m=})")

        prev_player = self.mark_selections.get(cur_mark, None)

        if prev_player is not None and prev_player != self.cur_player:
            raise IllegalMove(f"player cannot switch marks ({m=})")

    def _choose_mark_for_cur_player(self, m: Mark) -> None:
        """Declare a mark choice for the current player"""
        self.mark_selections[m] = self.cur_player 

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
            self._finish_game(Result.CAT_GAME)

    def apply_move(self, m: Move) -> None:
        self._check_game_state_pre_move(m)

        self._start_game_if_needed()
        
        self._check_mark_consistency(m)
        self._choose_mark_for_cur_player(m.mark)

        self.board.apply_move(m)

        self.move_history.append(m)

        self._adjust_game_state_post_move()

        if self.state == GameState.PLAYING:
            self._end_turn()
