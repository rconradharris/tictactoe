import sys

from interactive.loop import start_loop
from tests.runner import run_tests


def debug():
    """Place debug code here for one-off experiments"""
    pass


def main():
    if len(sys.argv) < 2:
        print("usage: main.py <play|test>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "play":
        start_loop()
    elif cmd == "debug":
        debug()
    elif cmd == "test":
        run_tests('tests')
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__":
    main()
