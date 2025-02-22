from dataclasses import dataclass, field

from at3.enums import GameChoice
from engine.enums import PlacementRule, Piece, Result
from engine.move import Move


@dataclass
class AT3Object:
    # Known Fields
    event: str = ""
    site: str = ""

    # Forward-compat: If we ever parse date into datetime object, it will go in the `date`
    # field
    date_str: str = ""

    player1: str = ""
    player2: str = ""

    result: Result = Result.UNDEFINED

    player1_elo: int = 0
    player2_elo: int = 0

    time_control: str = ""

    placement_rule: PlacementRule = PlacementRule.ANYWHERE

    # Grid field
    rows: int = 3
    cols: int = 3

    win_count: int = 3

    game_choice: GameChoice = GameChoice.UNDEFINED

    # Required Fields
    player1_choice: Piece = Piece._

    # All Fields (known and unknown)
    #
    # Dict preserves order so format(parse(data)) should mostly round-trip
    _fields: dict[str, str] = field(default_factory=dict)

    def set_field(self, field: str, value: str) -> None:
        self._fields[field] = value

    moves: list[Move] = field(default_factory=list)
