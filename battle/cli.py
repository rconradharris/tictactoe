from battle.battle import do_battle


def _battle(args) -> None:
    do_battle(
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
