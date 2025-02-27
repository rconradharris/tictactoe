from battle.battle import do_battle
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


def _battle(args) -> None:
    choice = _parse_game_choice(args.game)
    do_battle(
        choice=choice,
        num_games=args.num_games,
        p1_plies=args.p1_plies,
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
    p.add_argument(
        '--p1-plies',
        type=int,
        help='how deep player 1 searches',
    )
    p.add_argument(
        '--p2-plies',
        type=int,
        help='how deep player 1 searches',
    )
