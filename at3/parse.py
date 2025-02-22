import re

from at3.at3_object import AT3Object
from at3.exceptions import (
    ParseException,
    RequiredFieldMissing,
    UnknownFieldException,
)
from at3.enums import KnownField

from engine.enums import Mark, Player, Result


RE_META = re.compile(r'\s*\[(\w+)\s+\"(.+)\"\]\s*')

def _parse_meta(obj: AT3Object, line: str):
    if not line.endswith(']'):
        raise ParseException("meta line must end with ]")

    match = RE_META.match(line)
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
    elif f == KnownField.GRID:
        _parse_grid(obj, value)
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
    mark_str = value.upper()

    mark = Mark.from_str(mark_str)
    obj.player1_choice = mark


def _parse_grid(obj: AT3Object, value: str) -> None:
    if 'x' not in value:
        raise ParseException(
                f"'x' must be in grid field ({value=})")

    try:
        rows, cols = map(int, value.split('x'))
    except ValueError:
        raise ParseException(
                f"grid values must be numbers ({value=})")

    if rows != cols:
        raise ParseException(
                f"grid must be square ({value=})")

    obj.rows = rows
    obj.cols = cols


def _check_required_fields(obj: AT3Object) -> None:
    if obj.player1_choice == Mark._:
        raise RequiredFieldMissing("Player1Choice must be specified")


def parse(at3_data: str) -> AT3Object:
    obj = AT3Object()

    lines = at3_data.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("["):
            _parse_meta(obj, line)

    _check_required_fields(obj)
    return obj
