from game.first_move import FirstMove
from game.game_choice import GameChoice
from game.piece import Piece
from play.loop import start_loop


def _add_first_move(parser) -> None:
    choices = [x.pretty() for x in FirstMove.all()]
    parser.add_argument(
        '--first-move',
        '-f',
        default=FirstMove.COIN_TOSS.pretty(),
        choices=choices,
        help='who plays first, default is to use a coin toss',
    )


def _add_p1_piece(parser) -> None:
    choices = []

    # Allow for case-insensitive selection
    for p in Piece.selectable():
        s = p.pretty()
        choices.append(s)
        choices.append(s.lower())

    parser.add_argument(
        '--p1-piece',
        default=Piece.X.pretty(),
        choices=choices,
        help='which piece player 1 should use',
    )


def _add_game_choice(parser) -> None:
    choices = [x.abbrev() for x in GameChoice.selectable()]
    parser.add_argument(
        '--game',
        '-g',
        default=GameChoice.TIC_TAC_TOE.abbrev(),
        choices=choices,
        help='which game to play, tic-tac-toe or connect four',
    )


def _play(args) -> None:
    game_choice = GameChoice.from_abbrev(args.game)
    p1_piece = Piece.from_str(args.p1_piece.upper())
    first_move = FirstMove.from_str(args.first_move)

    start_loop(
        game_choice=game_choice,
        difficulty=args.difficulty,
        p1_piece=p1_piece,
        first_move=first_move,
    )


def add_subparser(subparsers) -> None:
    p = subparsers.add_parser(
        'play',
        aliases=['p'],
        help='play interactively',
    )
    p.set_defaults(func=_play)

    _add_game_choice(p)

    p.add_argument(
        '--difficulty',
        '-d',
        type=int,
        default=5,
        help='how difficult the computer opponent is, lower is easier',
    )

    _add_p1_piece(p)

    _add_first_move(p)
