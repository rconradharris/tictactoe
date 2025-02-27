from collections import Counter

from engine.randimaxer import Randimaxer
from engine.t3.farseer import T3Farseer
from game.board import Board
from engine.engine import Engine
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.piece import Piece
from game.player import Player
from game.result import Result


def do_battle(
        choice: GameChoice = GameChoice.TIC_TAC_TOE,
        num_games: int = 1,
        verbose: bool = True,
        ):
    """Have two engines play each other"""

    params = choice.parameters()
    assert params is not None
    b = Board.from_game_parameters(params)
    g = Game(b)

    p2eng: dict[Player, Engine] = {}
    p2eng[Player.P1] = Randimaxer(g, Player.P1)
    #p2eng[Player.P1] = T3Farseer(g, Player.P1)
    p2eng[Player.P2] = T3Farseer(g, Player.P2)

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

            if verbose:
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
