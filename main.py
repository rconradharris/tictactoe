import argparse
import logging

import battle.cli
import interactive.cli
import tests.cli


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def main():
    setup_logging()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    # Register subparsers for each command
    battle.cli.add_subparser(subparsers)
    interactive.cli.add_subparser(subparsers)
    tests.cli.add_subparser(subparsers)

    # Dispatch to command handler
    args = parser.parse_args()
    args.func(args)
    

if __name__ == "__main__":
    main()
