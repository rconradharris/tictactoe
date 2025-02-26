class GameException(Exception):
    pass


class IllegalMove(GameException):
    pass


class PieceSelectionException(GameException):
    pass


class PieceSelectionsAlreadyMade(PieceSelectionException):
    pass


class InvalidPieceSelection(PieceSelectionException):
    pass


class CellBoundsException(IllegalMove):
    pass
