Tic-Tac-Toe
===========

This project is a playground for exploring [m,n,k
games](https://en.wikipedia.org/wiki/M,n,k-game), including Tic-Tac-Toe and
Connect Four.

The different modules breakdown as:

- at3: implements a file format for recording m,n,k games. Think of this like
  chess' PGN, but for tic-tac-toe and its variants
- game: responsible for keeping track of game state, enforcing the rules and
  detecting wins or draws
- interactive: a simple CLI interface for playing a game
- tests: A test suite which uses AT3 to encode a set of test cases

Q & A
=====

Q. Isn't Tic-Tac-Toe solved and known to be a draw with perfect play? If so why
build a Python library to implement it?

A. Yes! But its simplicity makes it worth studying in order to understand more
complicated games like checkers and chess. The minimax algorithm or a
neural-net that can play Tic-Tac-Toe would be fun explorations. But they need a
library that implements the game, hence why this project exists.
