"""
Algebraic Tic-Tac-Toe (AT3) Notation

A standardized format for recording tic-tac-toe games inspired by PGN
notation.

Arbitrary metadata can be included using brackets.

One piece of specialized metadata is the grid specifier. If provided, an
arbitrary square grid can be used. If not specified, a 3x3 is assumed.

Columns are lettered left to right: a, b, c...
Rows are numbered top to bottom: 1, 2, 3...

Sample 
======

[Event "World Tic-Tac-Toe Championships"]   
[Date "2025.02.21"]   
[Grid "3x3"]
[Result "1-0"]
[Player1 "X"]

1. a1 2. b2
3. c2 ...


P.S. Yes this is a joke... ;-)
"""
class AT3Object:
    pass
