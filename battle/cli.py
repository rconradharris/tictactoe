from battle.battle import do_battle
from engine.engine_choice import EngineChoice
from game.game_choice import GameChoice


def _parse_game_choice(s: str) -> GameChoice:
    return GameChoice.from_abbrev(s)


def _add_game_choice(parser) -> None:
    choices = [x.abbrev() for x in GameChoice.selectable()]
    parser.add_argument(
        '--game',
        '-g',
        default=GameChoice.TIC_TAC_TOE.abbrev(),
        choices=choices,
        help='which game to play, tic-tac-toe or connect four',
    )

def _add_engine_options(parser) -> None:
    choices = [x.pretty() for x in EngineChoice]

    # Player 1
    parser.add_argument(
        '--p1-engine',
        default=EngineChoice.DUMMY.pretty(),
        choices=choices,
        help='which engine to use for player 1',
    )
    parser.add_argument(
        '--p1-plies',
        type=int,
        help='how deep player 1 searches',
    )

    # Player 2
    parser.add_argument(
        '--p2-engine',
        default=EngineChoice.WINIBETAMAXER.pretty(),
        choices=choices,
        help='which engine to use for player 2',
    )
    parser.add_argument(
        '--p2-plies',
        type=int,
        help='how deep player 1 searches',
    )


def _battle(args) -> None:
    game_choice = _parse_game_choice(args.game)
    p1_engine = EngineChoice.from_str(args.p1_engine)
    p2_engine = EngineChoice.from_str(args.p2_engine)

    do_battle(
        game_choice=game_choice,
        num_games=args.num_games,
        p1_engine=p1_engine,
        p1_plies=args.p1_plies,
        p2_engine=p2_engine,
        p2_plies=args.p2_plies,
        quiet=args.quiet,
    )


def add_subparser(subparsers) -> None:
    p = subparsers.add_parser(
        'battle',
        aliases=['b'],
        help='watch two engines do battle',
    )
    p.set_defaults(func=_battle)

    _add_game_choice(p)

    p.add_argument(
        '--num-games',
        '-n',
        type=int,
        default=1,
        help='number of times to do battle',
    )

    _add_engine_options(p)
