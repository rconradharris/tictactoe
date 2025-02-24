from game.board import Board
from game.enums import GameState, Piece
from game.exceptions import CellBoundsException, IllegalMove
from game.game import Game
from game.game_choice import GameChoice
from game.move import Move
from interactive.command import Command
from interactive.exceptions import ContinueLoop


def _show_board(g: Game):
    print(g.board.pretty(coords=True))
    print()


def _show_help() -> None:
    print("""\
GAME CHOICES
    T3 - Tic Tac Toe
    C4 - Connect Four

COMMANDS
    . - show board
    ? - display help

MOVE SYNTAX
    T3: <column-letter><row-number> (ex: 'a1')
    C4: <column-letter> (ex: 'a')""")


def _handle_commands(g: Game, cmd_str: str) -> None:
    try:
        cmd = Command.from_str(cmd_str)
    except ValueError:
        # Unrecognized commands should be ignored so they can be treated as
        # moves
        return

    if cmd == Command.SHOW_BOARD:
        _show_board(g)
        raise ContinueLoop
    elif cmd == Command.HELP:
        _show_help()
        raise ContinueLoop


def _parse_move_cell(g: Game, cell_str: str, cur_piece: Piece) -> Move:
    """Treat move as standard algebraic notation, e.g. 'a1'"""
    b = g.board
    sz = (b.rows, b.cols)

    try:
        cell = Board.parse_cell(cell_str, sz)
    except ValueError:
        # Try again
        print("error: invalid move syntax. (hint: 'a1')")
        raise ContinueLoop
    except CellBoundsException:
        # Try again
        print("error: move must be on the board (hint: 'a1')")
        raise ContinueLoop

    return Move(cell, cur_piece)


def _parse_move_c4(g: Game, cell_letter: str, cur_piece: Piece) -> Move:
    """
    Connect Four player specify the column only and the piece 'drops' into
    place, e.g. 'c'.
    """
    b = g.board
    sz = (b.rows, b.cols)

    try:
        col = Board.parse_column_letter(cell_letter, sz)
    except ValueError:
        # Try again
        print("error: invalid column selection (hint: 'a')")
        raise ContinueLoop
    except CellBoundsException:
        # Try again
        print("error: column selection must be on the board (hint: 'a')")
        raise ContinueLoop

    # This simulates gravity by placing the piece on the first not empty row
    # in that column
    row = g.board.top_empty_row_for_column(col)

    cell = (row, col)

    return Move(cell, cur_piece)


def _input_move(g: Game, move_num: int, choice: GameChoice, cur_piece: Piece) -> Move:

    cell_str = input(f"{move_num}. {cur_piece.pretty()} to Move: ")

    _handle_commands(g, cell_str)

    if choice == GameChoice.CONNECT_FOUR:
        move = _parse_move_c4(g, cell_str, cur_piece)
    else:
        move = _parse_move_cell(g, cell_str, cur_piece)

    return move


def _game_loop(g: Game, choice: GameChoice) -> None:
    while True:
        piece_str = input("Choose 'X' or 'O': ")
        piece_str = piece_str.upper()
        try:
            cur_piece = Piece.from_str(piece_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    _show_board(g)

    move_num = 1
    while True:
        if g.state == GameState.FINISHED:
            break

        try:
            move = _input_move(g, move_num, choice, cur_piece)
        except ContinueLoop:
            continue

        try:
            g.apply_move(move)
        except IllegalMove as e:
            # Try again
            print(e)
            continue

        _show_board(g)

        move_num += 1
        cur_piece = cur_piece.next()

    print(g.result)


def start_loop() -> None:
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
            size=params.size,
            win_count=params.win_count,
            placement_rule=params.placement_rule
        )

    g = Game(b)

    _game_loop(g, choice)
