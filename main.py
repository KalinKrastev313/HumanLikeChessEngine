import time

from engine import Engine
import chess
import chess.pgn
from chess.polyglot import MemoryMappedReader

def play_a_game():
    board = chess.Board()
    time_lst = []
    prev_move_played_at = time.time()
    opening_book_white = MemoryMappedReader('data/openings/white_repertoire.bin')
    opening_book_black = MemoryMappedReader('data/openings/black_repertoire.bin')
    engine_human = Engine(opening_book_white, opening_book_black)
    while not board.is_game_over():
        move = engine_human.suggest_move(board)
        board.push(move)
        game = chess.pgn.Game.from_board(board)
        print(game)
        move_duration = time.time() - prev_move_played_at
        time_lst.append(move_duration)
        print(move_duration)
        prev_move_played_at = time.time()

    game = chess.pgn.Game.from_board(board)
    print(time_lst)

    return str(game)


def save_the_game(pgn):
    with open('game_pgn.txt', 'w') as file:
        file.writelines(str(pgn))


if __name__ == '__main__':
    pgn = play_a_game()
    save_the_game(pgn)
