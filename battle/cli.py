from battle.battle import do_battle


def _battle(args) -> None:
    do_battle(num_games=args.num_games)


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
        default=1
    )
