"""
Algebraic Tic-Tac-Toe (AT3) Notation

A standardized format for recording tic-tac-toe games inspired by PGN
notation.

Arbitrary metadata can be included using brackets.

One piece of specialized metadata is the grid field. If provided, an
arbitrary square grid can be specifie, otherwise a 3x3 is assumed.

The only REQUIRED field is 'Player1Choice' which defines whether Player1
chooses Xs or Os (oh, oh, oh).

Columns are lettered left to right: a, b, c...
Rows are numbered top to bottom: 1, 2, 3...

Sample 
======

[Event "World Tic-Tac-Toe Championships"]
[Site "Los Angeles, CA, USA"]
[Date "2025.02.21"]
[Player1 "Alice Kasparov"]
[Player2 "Bob Carlsen"]
[Result "Cat Game"]
[Player1Elo "3000"]
[Player2Elo "3000"]
[TimeControl "Whenever"]
[Grid "3x3"]
[Player1Choice "X"]

1. a1 2. b2
3. c2 ...


P.S. Yes this is a joke... ;-)
"""
from dataclasses import dataclass, field

from engine.enums import Mark, Result


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

    # Grid field
    rows: int = 3
    cols: int = 3

    # Required Fields
    player1_choice: Mark = Mark._

    # All Fields (known and unknown)
    #
    # Dict preserves order so format(parse(data)) should mostly round-trip
    _fields: dict[str, str] = field(default_factory=dict)

    def set_field(self, field: str, value: str) -> None:
        self._fields[field] = value
