import argparse
import logging

import battle.cli
import play.cli
import tests.cli


def setup_logging(level):
    logging.basicConfig(level=level)


def add_global_args(parser):
    parser.add_argument(
        '--debug',
        action='store_true',
        help='enable debug logging',
    )

    # Verbosity is concerned with logging levels where as quietude is
    # concerned with how much output each subcommand chooses to display
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='be more quiet than usual',
    )


def handle_global_args(args):
    if args.debug:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.WARNING)


def main():
    parser = argparse.ArgumentParser()

    add_global_args(parser)

    subparsers = parser.add_subparsers(required=True)

    # Register subparsers for each command
    battle.cli.add_subparser(subparsers)
    play.cli.add_subparser(subparsers)
    tests.cli.add_subparser(subparsers)

    args = parser.parse_args()

    handle_global_args(args)

    # Dispatch to specific command handler
    args.func(args)
    

if __name__ == "__main__":
    main()
