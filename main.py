import sys

from battle.battle import do_battle
from interactive.loop import start_loop
from tests.file_tests import run_file_test
from tests.runner import run_tests


def debug():
    """Place debug code here for one-off experiments"""
    pass


def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        die("usage: main.py <play|test|tests>")

    cmd = sys.argv[1]
    if cmd == "play":
        start_loop()
    elif cmd == "debug":
        debug()
    elif cmd == "battle":
        # Single file test
        try:
            num_games = int(sys.argv[2])
        except IndexError:
            num_games = 1
        except ValueError:
            die("error: number of games must be a number")

        do_battle(num_games=num_games)
    elif cmd == "file_test":
        # Single file test
        try:
            filename = sys.argv[2]
        except IndexError:
            die("error: specify test filename")
        run_file_test(filename)
    elif cmd == "tests":
        # Full test suite
        run_tests()
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__":
    main()
