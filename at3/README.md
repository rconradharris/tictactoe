Algebraic Tic-Tac-Toe (AT3) Notation

A standardized format for recording tic-tac-toe games inspired by PGN notation.
More generally, AT3 supports most other m,n,k games using the `Grid` and `Win
Count` fields. Connect Four is supported by setting `PlacementRule` to
`ColumnStack`.

Arbitrary metadata can be included using brackets.

Grid Size
=========

To specify an arbtrary grid size, for example 5x4, use `[Grid "5x4"]`.

Make sure to use the `.at3` extension for the filename since `.t3` is reserved
for standard 3x3 tic-tac-toe.

Required Fields
===============

The only required field is 'Player1Choice' which defines whether Player1
chooses Xs or Os (oh, oh, oh).

Moves
=====

Moves are recorded in algebraic notation like a chess board. Columns (files)
are lettered, rows (ranks) are numbered. So an example move list would be:

1. a2 2. b1


File Extension
==============

AT3 file use the '.at3' extension as a default. This supports arbitrary m,n,k style games.

You can use '.t3' as a short-hand for tic-tac-toe and this will apply those
game parameters.

Likewise, you can use '.c4' as a short-hand for Connect Four.

Sample 
======

```
    [Event "World Tic-Tac-Toe Championships"]
    [Site "Los Angeles, CA, USA"]
    [Date "2025.02.21"]
    [Game "TicTacToe"]
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
```
