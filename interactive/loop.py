from engine.engine import Engine
from engine.mnk.dummy import Dummy
from engine.mnk.winimaxer import Winimaxer
from game.board import Board
from game.exceptions import CellBoundsException, IllegalMove
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.move import Move
from game.piece import Piece
from game.placement_rule import PlacementRule
from game.player import Player
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


def _pick_engine(g: Game, p: Player, level: int) -> Engine:
    if level == 1:
        return Dummy(g, p)

    max_plies = level - 1
    return Winimaxer(g, p, max_plies=max_plies)


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


def _input_difficulty_level() -> int:
    diff = 0

    while True:
        s = input("Choose difficulty level [1-10]: ")
        try:
            diff = int(s)
        except ValueError:
            # Try again
            print("error: difficulty must be between 1 and 10")
            continue
        else:
            break

    return diff


def _input_player1_piece() -> Piece:
    p = Piece._

    while True:
        s = input("Choose 'X' or 'O': ")
        s = s.upper()
        try:
            p = Piece.from_str(s)
        except ValueError as e:
            # Try again
            print(e)
            continue
        else:
            break

    assert p != Piece._
    return p


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
        b = Board.from_game_parameters(params)

    g = Game(b)

    player1_piece = _input_player1_piece()
    g.choose_player1_piece(player1_piece)

    level = _input_difficulty_level()

    # FIXME: right now the engine is always player 2, but this should be
    # configurable
    eng = _pick_engine(g, Player.P2, level)

    _show_board(g.board)

    _game_loop(g, eng)
