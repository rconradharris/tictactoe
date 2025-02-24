from game.board import Board
from game.exceptions import CellBoundsException, IllegalMove
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.move import Move
from game.piece import Piece
from game.placement_rule import PlacementRule
from game.typedefs import Cell
from interactive.command import Command
from interactive.exceptions import ContinueLoop


def _show_board(b: Board) -> None:
    print(b.pretty(coords=True))
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


def _handle_commands(b: Board, cmd_str: str) -> None:
    try:
        cmd = Command.from_str(cmd_str)
    except ValueError:
        # Unrecognized commands should be ignored so they can be treated as
        # moves
        return

    if cmd == Command.SHOW_BOARD:
        _show_board(b)
        raise ContinueLoop
    elif cmd == Command.HELP:
        _show_help()
        raise ContinueLoop


def _parse_piece_placement(b: Board, cell_str: str) -> Cell:
    """Treat move as standard algebraic notation, e.g. 'a1'"""
    try:
        return b.parse_piece_placement(cell_str)
    except ValueError:
        # Try again
        print("error: invalid move syntax. (hint: 'a1')")
        raise ContinueLoop
    except CellBoundsException:
        # Try again
        print("error: move must be on the board (hint: 'a1')")
        raise ContinueLoop


def _input_move(b: Board, move_num: int, cur_piece: Piece) -> Cell:

    if b.placement_rule == PlacementRule.COLUMN_STACK:
        hint = "type a column letter"
    else:
        hint = "type a coordinate like 'a1'"

    cell_str = input(f"{move_num}. {cur_piece.pretty()} to Move (hint: {hint}): ")

    _handle_commands(b, cell_str)

    return _parse_piece_placement(b, cell_str)


def _game_loop(g: Game) -> None:
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

    _show_board(g.board)

    move_num = 1
    while True:
        if g.state == GameState.FINISHED:
            break

        try:
            cell = _input_move(g.board, move_num, cur_piece)
        except ContinueLoop:
            continue

        move = Move(cell, cur_piece)

        try:
            g.apply_move(move)
        except IllegalMove as e:
            # Try again
            print(e)
            continue

        _show_board(g.board)

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

    _game_loop(g)
