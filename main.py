import time

from engine import Engine
import chess
import chess.pgn


def play_a_game():
    board = chess.Board()
    time_lst = []
    begin =time_lst.append(time.time())
    while not board.is_game_over():
        engine_human = Engine()
        move = engine_human.suggest_move(board)
        board.push(move)
        time_lst.append(time.time())
        game = chess.pgn.Game.from_board(board)
        print(game)

    game = chess.pgn.Game.from_board(board)
    print(time_lst)

    return str(game)


def save_the_game(pgn):
    with open('game_pgn.txt', 'w') as file:
        file.writelines(str(pgn))


if __name__ == '__main__':
    pgn = play_a_game()
    save_the_game(pgn)
