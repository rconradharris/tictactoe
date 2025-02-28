from enum import Enum, auto


class PieceFormat(Enum):
    ASCII_X_O = auto()
    RED_YELLOW_CIRCLES = auto()
    EMOJI_X_O = auto()


class Piece(Enum):
    _ = auto()
    X = auto()
    O = auto()  # noqa: E741 (typographically ambiguous with zero, but thats okay)

    @classmethod
    def selectable(cls) -> list["Piece"]:
        return [cls.X, cls.O]

    def _pretty_ascii_x_o(self) -> str:
        if self == self._:
            return "_"
        elif self == self.X:
            return "X"
        elif self == self.O:
            return "O"

        return "?"

    def _pretty_red_yellow_circles(self) -> str:
        if self == self._:
            return "_"
        elif self == self.X:
            return "🔴"
        elif self == self.O:
            return "🟡"

        return "?"

    def _pretty_emoji_x_o(self) -> str:
        if self == self._:
            return "⬛"
        elif self == self.X:
            return "❌"
        elif self == self.O:
            return "⭕"

        return "?"

    def pretty(self, fmt: PieceFormat = PieceFormat.ASCII_X_O) -> str:
        if fmt == PieceFormat.ASCII_X_O:
            return self._pretty_ascii_x_o()
        elif fmt == PieceFormat.RED_YELLOW_CIRCLES:
            return self._pretty_red_yellow_circles()
        elif fmt == PieceFormat.EMOJI_X_O:
            return self._pretty_emoji_x_o()

        return "?"

    @classmethod
    def from_str(cls, s: str) -> "Piece":
        if s == "_":
            return cls._
        elif s == "X":
            return cls.X
        elif s == "O":
            return cls.O

        raise ValueError(f"unknown piece: '{s}'")

    def next(self) -> "Piece":
        """Returns the next piece in the sequence, i.e. X -> O"""
        if self == Piece.X:
            return Piece.O
        elif self == Piece.O:
            return Piece.X

        raise Exception("only X and O pieces are sequencable")
