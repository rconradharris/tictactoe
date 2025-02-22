import sys

from engine.board import Board
from engine.enums import GameState, Piece
from engine.exceptions import IllegalMove
from engine.game import Game
from engine.game_choice import GameChoice
from engine.move import Move
from tests.runner import run_tests


def show_board(g: Game):
    print(f"{g.cur_player} {g.state} {g.result}")
    print(g.board.pretty(coords=True))
    print()

def show_help() -> None:
    print("""\
GAME CHOICES
    T3 - Tic Tac Toe
    C4 - Connect Four

COMMANDS
    . - show board
    ? - display help

MOVE SYNTAX
    <column-letter><row-number> (ex: 'a1')""")


def game_loop(g: Game) -> None:
    CMD_SHOW_BOARD = "."
    CMD_HELP = "?"

    show_board(g)

    while True:
        piece_str = input('X or O? ')
        piece_str = piece_str.upper()
        try:
            cur_piece = Piece.from_str(piece_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    move_num = 1
    while True:
        if g.state == GameState.FINISHED:
            break

        cell_str = input(f"{move_num}. Move? ")

        if cell_str == CMD_SHOW_BOARD:
            show_board(g)
            continue
        elif cell_str == CMD_HELP:
            show_help()
            continue

        try:
            cell = Board.parse_algebraic_cell(cell_str)
        except ValueError as e:
            # Try again
            print(e)
            continue

        move = Move(cell, cur_piece)

        try:
            g.apply_move(move)
        except IllegalMove as e:
            # Try again
            print(e)
            continue

        show_board(g)

        move_num += 1
        cur_piece = cur_piece.next()

    print(g.result)


def interactive() -> None:
    while True:
        choice_str = input('Tic-Tac-Toe or Connect Four (T3 or C4)? ')
        try:
            choice = GameChoice.from_abbrev(choice_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    b = Board()

    params = choice.parameters()
    if params:
        b = Board(
            rows=params.rows,
            cols=params.cols,
            win_count=params.win_count,
            placement_rule=params.placement_rule
        )

    g = Game(b)

    game_loop(g)


def main():
    if len(sys.argv) < 2:
        print("usage: main.py <play|test>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "play":
        interactive()
    elif cmd == "test":
        run_tests('tests')
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__":
    main()
