from engine.board import Board
from engine.enums import GameState, Mark, Player
from engine.exceptions import IllegalMove
from engine.move import Move

class Game:
    """
    Game ends with either WON or a CAT_GAME. The current player is declared
    the winner if the state is WON.
    """

    def __init__(self, board: Board):
        self.board: Board = board
        self.reset()

    def reset(self):
        self.cur_player: Player = Player.P1
        self.mark_selections: dict[Mark, Player] = {}
        self.state: GameState = GameState.INIT
        self.move_history: list[Move] = []

    def _end_turn(self):
        if self.cur_player == Player.P1:
            self.cur_player = Player.P2
        else:
            self.cur_player = Player.P1

    def _check_mark_consistency(self, m: Move):
        """Ensure players cannot switch marks once they've chosen"""
        cur_mark = m.mark

        if cur_mark == Mark._:
            raise IllegalMove(f"mark cannot be blank ({m=})")

        prev_player = self.mark_selections.get(cur_mark, None)

        if prev_player is not None and prev_player != self.cur_player:
            raise IllegalMove(f"player cannot switch marks ({m=})")

    def _choose_mark_for_cur_player(self, m: Mark):
        """Declare a mark choice for the current player"""
        self.mark_selections[m] = self.cur_player 

    def _check_game_state_pre_move(self, m: Move):
        if self.state == GameState.WON:
            raise IllegalMove(f"cannot move after a game was won ({m=})")
        elif self.state == GameState.CAT_GAME:
            raise IllegalMove(f"cannot move after a game terminated ({m=})")

    def _start_game_if_needed(self):
        if self.state == GameState.INIT:
            self.state = GameState.PLAYING

    def _adjust_game_state_post_move(self):
        if self.board.win():
            self.state = GameState.WON
        elif self.board.full():
            self.state = GameState.CAT_GAME

    def apply_move(self, m: Move):
        self._check_game_state_pre_move(m)

        self._start_game_if_needed()
        
        self._check_mark_consistency(m)
        self._choose_mark_for_cur_player(m.mark)

        self.board.apply_move(m)

        self.move_history.append(m)

        self._adjust_game_state_post_move()

        if self.state == GameState.PLAYING:
            self._end_turn()
