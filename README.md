Tic-Tac-Toe
===========

This project is a playground for exploring [m,n,k
games](https://en.wikipedia.org/wiki/M,n,k-game), including Tic-Tac-Toe and
Connect Four.

The different modules breakdown as:

- at3: implements a file format for recording m,n,k games. Think of this like
  chess' PGN, but for tic-tac-toe and its variants
- engine: implements various m,n,k playing engines using a variety of
  strategies, including minimax
- game: responsible for keeping track of game state, enforcing the rules and
  detecting wins or draws
- play: a simple CLI interface for playing a game
- tests: A test suite which uses AT3 to encode a set of test cases


Things to Try
=============

- `uv run main.py play` to play interactively
- `uv run main.py battle -n 5` to watch two engines battle it out 5 times, tic-tac-toe is the default game
- `uv run main.py battle -g c4 -n 5 --p2-plies 3` to watch two engines play Connect Four 5 times, player 2 only looks ahead 3 moves (plies)
- `uv run main.py tests` to run the unit and file-based test suites


Q & A
=====

Q. Isn't Tic-Tac-Toe solved and known to be a draw with perfect play? If so why
build a Python library to implement it?

A. Yes! But its simplicity makes it worth studying in order to understand more
complicated games like checkers and chess. The minimax algorithm or a
neural-net that can play Tic-Tac-Toe would be fun explorations. But they need a
library that implements the game, hence why this project exists.
