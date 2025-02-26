from collections import Counter
import sys

from game.result import Result
from interactive.loop import start_loop
from tests.file_tests import run_file_test
from tests.runner import run_tests


def debug():
    """Place debug code here for one-off experiments"""
    pass


def battle(num_games: int = 1):
    """Have two engines play each other"""
    from engine.minimax import RandiMaxer
    from game.board import Board
    from engine.engine import Engine
    from game.game import Game, GameState
    from game.game_choice import GameChoice
    from game.piece import Piece
    from game.player import Player

    #choice = GameChoice.TIC_TAC_TOE
    choice = GameChoice.CONNECT_FOUR
    params = choice.parameters()
    assert params is not None
    b = Board.from_game_parameters(params)
    g = Game(b)

    p2eng: dict[Player, Engine] = {}
    p2eng[Player.P1] = RandiMaxer(g, Player.P1)
    p2eng[Player.P2] = RandiMaxer(g, Player.P2)

    result_stats: Counter = Counter()

    for i in range(num_games):
        game_num = i + 1
        g.reset()
        g.choose_player1_piece(Piece.X)

        # Play until each game is done
        while g.state != GameState.FINISHED:
            eng = p2eng[g.cur_player]
            m = eng.generate_move()

            g.apply_move(m)

            print(f"{g.state=} {g.result=}")
            print(g.board.pretty(coords=True))
            print()

        print(f"Game {game_num}/{num_games} result: {g.result}")
        result_stats[g.result] += 1

    print("=== Stats ===")
    print_result_stat(result_stats, Result.PLAYER1_VICTORY, num_games)
    print_result_stat(result_stats, Result.PLAYER2_VICTORY, num_games)
    print_result_stat(result_stats, Result.DRAW, num_games)


def print_result_stat(result_stats: Counter, r: Result, total: int) -> None:
    count = result_stats[r]
    rate = count / total
    pct = rate * 100

    print(f"{r}: {pct:.1f}")


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
        battle()
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
