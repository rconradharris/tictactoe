import re

from at3.at3_object import AT3Object
from at3.exceptions import (
    ParseException,
    ParseStateException,
    RequiredFieldMissing,
    UnknownFieldException,
)
from at3.enums import KnownField, ParseState
from at3.file_extensions import game_choice_from_extension

from engine.board import Board
from engine.enums import Player, Piece, Result
from engine.game_choice import GameChoice
from engine.move import Move
from engine.placement_rule import PlacementRule


RE_METADATA_LINE = re.compile(r'\s*\[(\w+)\s+\"(.+)\"\]\s*')

def _parse_metadata_line(obj: AT3Object, line: str):
    if not line.endswith(']'):
        raise ParseException("meta line must end with ]")

    match = RE_METADATA_LINE.match(line)
    if not match:
        raise ParseException(f"syntax error in meta line {line=}")

    # Add all known and unknown fields to `_fields` dict
    field_name, field_value = match.groups()
    obj.set_field(field_name, field_value)

    # Known fields get first-class attributes of proper type
    try:
        field = KnownField.from_str(field_name)
    except UnknownFieldException:
        pass
    else:
        _parse_known_field(obj, field, field_value)


def _parse_known_field(obj: AT3Object, f: KnownField, value: str) -> None:
    if f == KnownField.EVENT:
        obj.event = value
    elif f == KnownField.SITE:
        obj.site = value
    elif f == KnownField.DATE:
        obj.date_str = value
    elif f == KnownField.PLAYER1:
        obj.player1 = value
    elif f == KnownField.PLAYER2:
        obj.player2 = value
    elif f == KnownField.RESULT:
        _parse_result(obj, value)
    elif f == KnownField.PLAYER1_ELO:
        _parse_player_elo(obj, Player.P1, value)
    elif f == KnownField.PLAYER2_ELO:
        _parse_player_elo(obj, Player.P2, value)
    elif f == KnownField.TIME_CONTROL:
        obj.time_control = value
    elif f == KnownField.PLACEMENT_RULE:
        _parse_placement_rule(obj, value)
    elif f == KnownField.GRID:
        _parse_grid(obj, value)
    elif f == KnownField.WIN_COUNT:
        _parse_win_count(obj, value)
    elif f == KnownField.GAME_CHOICE:
        _parse_game_choice(obj, value)
    elif f == KnownField.PLAYER1_CHOICE:
        # The one required field
        _parse_player1_choice(obj, value)


def _parse_result(obj: AT3Object, value: str) -> None:
    result = Result.from_str(value)
    obj.result = result


def _parse_player_elo(obj: AT3Object, p: Player, value: str) -> None:
    try:
        elo = int(value)
    except ValueError:
        raise ParseException(f"elo must be a number ({value=})")

    if p == Player.P1:
        obj.player1_elo = elo
    elif p == Player.P2:
        obj.player2_elo = elo
    else:
        raise ParseException(f"unknown player ({p=})")


def _parse_player1_choice(obj: AT3Object, value: str) -> None:
    piece_str = value.upper()

    piece = Piece.from_str(piece_str)
    obj.player1_choice = piece


def _parse_placement_rule(obj: AT3Object, value: str) -> None:
    obj.placement_rule = PlacementRule.from_str(value)


def _parse_grid(obj: AT3Object, value: str) -> None:
    """
    Like 7x6 corresponding to 7 columns by 6 rows.
    """
    if 'x' not in value:
        raise ParseException(
                f"'x' must be in grid field ({value=})")

    try:
        cols, rows = map(int, value.split('x'))
    except ValueError:
        raise ParseException(
                f"grid values must be numbers ({value=})")

    obj.rows = rows
    obj.cols = cols


def _parse_game_choice(obj: AT3Object, value: str) -> None:
    obj.game_choice = GameChoice.from_str(value)


def _parse_win_count(obj: AT3Object, value: str) -> None:
    try:
        win_count = int(value)
    except ValueError:
        raise ParseException(
                f"win count must be a number ({value=})")

    if win_count <= 0:
        raise ParseException(
                f"win count must be greater than zero ({value=})")

    obj.win_count = win_count


def parse(at3_data: str, path: str | None = None) -> AT3Object:
    """Convenience function to parse"""
    parser = Parser()
    return parser.parse(at3_data, path=path)


class Parser:

    def __init__(self) -> None:
        self.state: ParseState = ParseState.INIT
        self.cur_piece: Piece = Piece._
        self.prev_move_num: int = 0

    def _check_state(self, allowed: list[ParseState], msg: str) -> None:
        state = self.state
        if state in allowed:
            return

        raise ParseStateException(f"{msg} ({state=})")

    def _check_metadata_state(self) -> None:
        """Ensure we're allowed to parse a metadata line"""
        allowed = [ParseState.INIT, ParseState.METADATA]
        msg = "cannot parse metadata in this state"

        self._check_state(allowed, msg)

    def _check_move_state(self, obj: AT3Object) -> None:
        """Ensure we're allowed to parse a move line"""
        self._check_player_choice_specified(obj)

        allowed = [ParseState.INIT, ParseState.METADATA,
                   ParseState.MOVE_NUMBER]
        msg = "cannot parse moves in this state"

        self._check_state(allowed, msg)

    def _parse_move_number(self, token: str) -> int:
        """Token is like '1.' """
        if '.' not in token:
            raise ParseException(f"move number must have a '.' ({token=})")

        move_num_str = token.replace('.', '')

        try:
            move_num = int(move_num_str)
        except ValueError:
            raise ParseException(f"move number must be a valid number ({token=})")

        if move_num < 1:
            raise ParseException(f"move number must start at 1 ({token=})")

        return move_num

    def _check_move_number_monotonic(self, move_num: int) -> None:
        prev_move_num = self.prev_move_num
        if (move_num - prev_move_num) != 1:
            raise ParseException(f"move number must increase by 1 each time"
                                 f" ({prev_move_num=} {move_num=})")
    def _parse_move_line(self, obj: AT3Object, line: str) -> None:
        """
        1. a1 2. b2
        """
        tokens = line.split(" ")

        for token in tokens:
            if self.state == ParseState.MOVE_NUMBER:
                move_num = self._parse_move_number(token)

                self._check_move_number_monotonic(move_num)

                self.prev_move_num = move_num

                self.state = ParseState.MOVE_CELL
            elif self.state == ParseState.MOVE_CELL:
                sz = (obj.rows, obj.cols)
                cell = Board.parse_cell(token, sz)

                move = Move(cell, self.cur_piece)
                obj.moves.append(move)

                self.cur_piece = self.cur_piece.next()

                self.state = ParseState.MOVE_NUMBER

    def _check_player_choice_specified(self, obj: AT3Object) -> None:
        if obj.player1_choice == Piece._:
            raise RequiredFieldMissing("Player1Choice must be specified")

    def _check_required_fields(self, obj: AT3Object) -> None:
        self._check_player_choice_specified(obj)

    def _apply_game_choice(self, obj: AT3Object) -> None:
        params = obj.game_choice.parameters()
        if params:
            obj.rows = params.rows
            obj.cols = params.cols
            obj.win_count = params.win_count
            obj.placement_rule = params.placement_rule

    def parse(self, at3_data: str, path: str | None = None) -> AT3Object:
        if self.state != ParseState.INIT:
            raise ParseStateException("must parse from an initialized state")

        obj = AT3Object()

        if path:
            obj.game_choice = game_choice_from_extension(path)

        lines = at3_data.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("["):
                self._check_metadata_state()
                self.state = ParseState.METADATA

                _parse_metadata_line(obj, line)
            else:
                if self.cur_piece == Piece._:
                    self.cur_piece = obj.player1_choice

                self._check_move_state(obj)
                self.state = ParseState.MOVE_NUMBER

                self._parse_move_line(obj, line)

        self.state = ParseState.DONE
        self._apply_game_choice(obj)
        self._check_required_fields(obj)
        return obj
