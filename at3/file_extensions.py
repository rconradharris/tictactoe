import os

from at3.enums import GameChoice

_extensions: dict[str, GameChoice] = {
    ".at3": GameChoice.UNDEFINED,
    ".ttt": GameChoice.TIC_TAC_TOE,
    ".c4": GameChoice.CONNECT_FOUR,
}


def valid_file_extension(path: str) -> bool:
    """Returns True if the path has a valid AT3 extension"""
    _, ext = os.path.splitext(path)
    return ext in _extensions


def game_choice_from_extension(path: str) -> GameChoice:
    _, ext = os.path.splitext(path)
    try:
        return _extensions[ext]
    except KeyError:
        return GameChoice.UNDEFINED
