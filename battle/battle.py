from collections import Counter

from engine.engine import Engine
from engine.mnk.dummy import Dummy
from engine.mnk.winibetamaxer import Winibetamaxer
from game.board import Board
from game.game import Game, GameState
from game.game_choice import GameChoice
from game.piece import Piece
from game.player import Player
from game.result import Result


def do_battle(
        choice: GameChoice = GameChoice.TIC_TAC_TOE,
        num_games: int = 1,
        p1_plies: int | None = None,
        p2_plies: int | None = None,
        quiet: bool = False,
        ):
    """Have two engines play each other

    :param num_games: number of times to do battle
    :param p1_plies: how deep player 1 searches
    :param p2_plies: how deep player 2 searches
    :param quiet: just show stats at the end
    """

    params = choice.parameters()
    assert params is not None
    b = Board.from_game_parameters(params)
    g = Game(b)

    eng_map: dict[Player, Engine] = {}

    p1eng = Dummy(g, Player.P1)
    eng_map[Player.P1] = p1eng

    #p2eng = Winimaxer(g, Player.P2, max_plies=p2_plies)
    p2eng = Winibetamaxer(g, Player.P2, max_plies=p2_plies)
    eng_map[Player.P2] = p2eng

    result_stats: Counter = Counter()

    for i in range(num_games):
        game_num = i + 1
        g.reset()
        g.choose_player1_piece(Piece.X)

        # Play until each game is done
        while g.state != GameState.FINISHED:
            eng = eng_map[g.cur_player]
            m = eng.generate_move()

            g.apply_move(m)

            if not quiet:
                print(f"{g.state=} {g.result=}")
                print(g.board.pretty(coords=True))
                print()

        if not quiet:
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

    print(f"{r:<24}: {count} ({pct:.1f} %)")
