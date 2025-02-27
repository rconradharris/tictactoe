from interactive.loop import start_loop


def _play(args) -> None:
    start_loop()


def add_subparser(subparsers) -> None:
    p = subparsers.add_parser(
        'play',
        aliases=['p'],
        help='play interactively',
    )
    p.set_defaults(func=_play)
