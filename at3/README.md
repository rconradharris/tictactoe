Algebraic Tic-Tac-Toe (AT3) Notation

A standardized format for recording tic-tac-toe games inspired by PGN
notation. More generally, AT3 supports most other m,n,k games using the `Grid`
and `Win Count` fields.

Arbitrary metadata can be included using brackets.

One piece of specialized metadata is the grid field. If provided, an
arbitrary square grid can be specifie, otherwise a 3x3 is assumed.

The only REQUIRED field is 'Player1Choice' which defines whether Player1
chooses Xs or Os (oh, oh, oh).

Columns are lettered left to right: a, b, c...
Rows are numbered top to bottom: 1, 2, 3...

File Extension
==============

AT3 file use the '.at3' extension as a default. This supports arbitrary m,n,k style games.

You can use '.ttt' as a short-hand for tic-tac-toe and this will
apply those game parameters.

Likewise, you can use '.c4' as a short-hand for Connect Four.

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
[PlacementRule "Anywhere"]
[Grid "3x3"]
[WinCount "3"]
[Player1Choice "X"]

1. a1 2. b2
3. c2 ...


P.S. Yes this is a joke... or is it?
