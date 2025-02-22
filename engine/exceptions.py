class EngineException(Exception):
    pass


class IllegalMove(EngineException):
    pass


class CellBoundsException(IllegalMove):
    pass
