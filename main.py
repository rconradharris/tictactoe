import sys

from interactive.loop import start_loop
from tests.runner import run_test, run_tests


def debug():
    """Place debug code here for one-off experiments"""
    from engine.minimax import best_move, rand_eval
    from game.board import Board
    from game.game import Game, GameState
    from game.game_choice import GameChoice
    from game.piece import Piece

    choice = GameChoice.TIC_TAC_TOE
    params = choice.parameters()
    b = Board.from_game_parameters(params)
    g = Game(b)
    g.choose_player1_piece(Piece.X)

    fn = rand_eval
    num_plies = 2

    print(g.board.pretty(coords=True))

    while g.state != GameState.FINISHED:
        m = best_move(g, num_plies, fn)
        g.apply_move(m)

        print(f"{g.state=} {g.result=}")
        print(g.board.pretty(coords=True))
        print()


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
    elif cmd == "test":
        # Single test
        try:
            filename = sys.argv[2]
        except IndexError:
            die("error: specify test filename")
        run_test(filename)
    elif cmd == "tests":
        # Full test suite
        run_tests('tests')
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__":
    main()
