from engine import Engine
import chess
import chess.pgn


def play_a_game():
    board = chess.Board()

    while not board.is_game_over():
        engine_human = Engine()
        move = engine_human.suggest_move(board)
        board.push(move)
        game = chess.pgn.Game.from_board(board)
        print(game)

    game = chess.pgn.Game.from_board(board)

    return str(game)


def save_the_game(pgn):
    with open('game_pgn.txt', 'w') as file:
        file.writelines(str(pgn))


if __name__ == '__main__':
    pgn = play_a_game()
    save_the_game(pgn)
