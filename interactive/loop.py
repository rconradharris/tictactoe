from engine.engine import Engine
from engine.t3.dummy import T3Dummy
from engine.c4.dummy import C4Dummy
from game.board import Board
from game.exceptions import CellBoundsException, IllegalMove
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.move import Move
from game.piece import Piece
from game.placement_rule import PlacementRule
from game.player import Player
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


def _parse_move(g: Game, cell_str: str) -> Move:
    """Treat move as standard algebraic notation, e.g. 'a1'"""
    try:
        return g.create_move(cell_str)
    except ValueError:
        # Try again
        print("error: invalid move syntax. (hint: 'a1')")
        raise ContinueLoop
    except CellBoundsException:
        # Try again
        print("error: move must be on the board (hint: 'a1')")
        raise ContinueLoop


def _input_move(g: Game) -> Move:
    pr = g.board.placement_rule
    if pr == PlacementRule.COLUMN_STACK:
        hint = "type a column letter"
    else:
        hint = "type a coordinate like 'a1'"

    cell_str = input(f"{g.move_num}. {g.cur_piece.pretty()} to Move (hint: {hint}): ")

    _handle_commands(g.board, cell_str)

    return _parse_move(g, cell_str)


def _pick_engine(g: Game, p: Player.P2) -> Engine:
    """
    We pick the engine based on PlacementRule rather GameChoice because we
    want the same engine to play grid sizes. So, for example, the even though
    its called the T3 engine, it can also play 4x4 grids. It's characteristic
    is playing a move ANYHWERE.

    Simiarly, the C4 engine can play any size Connect Four board. It's
    characteristic is placing pieces in a ColumnStack.
    """
    pr = g.board.placement_rule
    if pr == PlacementRule.ANYWHERE:
        return T3Dummy(g, p)
    elif pr == PlacementRule.COLUMN_STACK:
        return C4Dummy(g, p)

    raise ValueError("no engine found for placement rule")


def _game_loop(g: Game, eng: Engine) -> None:
    while True:
        if g.state == GameState.FINISHED:
            break

        if eng.player == g.cur_player:
            move = eng.generate_move()
        else:
            try:
                move = _input_move(g)
            except ContinueLoop:
                continue

        try:
            g.apply_move(move)
        except IllegalMove as e:
            # Try again
            print(e)
            continue

        _show_board(g.board)

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

    while True:
        piece_str = input("Choose 'X' or 'O': ")
        piece_str = piece_str.upper()
        try:
            player1_piece = Piece.from_str(piece_str)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    g.choose_player1_piece(player1_piece)

    # FIXME: right now the engine is always player 2, but this should be
    # configurable
    eng = _pick_engine(g, Player.P2)

    _show_board(g.board)

    _game_loop(g, eng)
