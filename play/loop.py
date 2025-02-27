from random import choice

from engine.engine import Engine
from engine.mnk.dummy import Dummy
from engine.mnk.winimaxer import Winimaxer
from game.board import Board
from game.exceptions import CellBoundsException, IllegalMove
from game.first_move import FirstMove
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.move import Move
from game.piece import Piece
from game.placement_rule import PlacementRule
from game.player import Player
from play.command import Command
from play.exceptions import ContinueLoop


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


def _pick_engine(g: Game, first_move: FirstMove, difficulty: int) -> Engine:
    if first_move == FirstMove.HUMAN:
        p = Player.P2
    elif first_move == FirstMove.ENGINE:
        p = Player.P1
    elif  first_move == FirstMove.COIN_TOSS:
        p = choice([Player.P1, Player.P2])
    else:
        raise Exception('unknown first move value')

    if difficulty == 1:
        return Dummy(g, p)

    max_plies = difficulty - 1
    return Winimaxer(g, p, max_plies=max_plies)


def _print_result(g: Game, eng: Engine) -> None:
    winner = g.winner()
    if winner is None:
        if g.board.placement_rule == PlacementRule.COLUMN_STACK:
            # Connect Four like
            print("Draw!")
        else:
            # Tic-tac-toe like
            print("Cat game!")
    elif winner == eng.player:
        print("You lose!")
    else:
        print("You win!")


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

    _print_result(g, eng)


def start_loop(
        game_choice: GameChoice = GameChoice.TIC_TAC_TOE,
        difficulty: int = 5,
        p1_piece: Piece = Piece.X,
        first_move: FirstMove = FirstMove.COIN_TOSS,
        ) -> None:

    """
    :param game_choice: which game to play
    :param difficulty: how strong the engine is, a proxy for algorithm and
    max_plies
    :param p1_piece: whether player 1 is 'X' or 'O'
    :param first_move: whether the engine or human goes first, or coin toss
    """
    b = Board()

    params = game_choice.parameters()
    if params:
        b = Board.from_game_parameters(params)

    g = Game(b)

    g.choose_player1_piece(p1_piece)

    eng = _pick_engine(g, first_move, difficulty)

    _show_board(g.board)

    _game_loop(g, eng)
