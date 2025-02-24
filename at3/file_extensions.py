import os

from game.game_choice import GameChoice

_extensions: dict[str, GameChoice] = {
    ".at3": GameChoice.UNDEFINED,
    ".t3": GameChoice.TIC_TAC_TOE,
    ".c4": GameChoice.CONNECT_FOUR,
}


def valid_file_extension(path: str) -> bool:
    """Returns True if the path has a valid AT3 extension"""
    _, ext = os.path.splitext(path)
    return ext in _extensions


def game_choice_from_extension(path: str) -> GameChoice:
    """For convenience, the file extension can be used to indicate what kind
    of game you're playing.

    Use .c4 for a Connect Four game, or .t3 for 3x3 Tic Tac Toe. For arbitrary
    m,n,k games use the .at3 extension.
    """
    _, ext = os.path.splitext(path)
    try:
        return _extensions[ext]
    except KeyError:
        return GameChoice.UNDEFINED
