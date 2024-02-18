import chess
from chess.polyglot import zobrist_hash, open_reader

from EvalCollector.polyglot_writer import Polyglot_Move, Polyglot_Position, Polyglot_Writer
# import struct


class EvalCollector:
    def __init__(self, board: chess.Board):
        self.board = board

    def check_for_prev_eval(self):
        prev_board = self.board.copy()
        prev_board.pop()
        with open_reader('EvalCollector\example.bin') as reader:
            pos_record = reader.get(prev_board)
            if pos_record:
                return pos_record.weight
        # try:
        #     with open('EvalCollector\data\zob_hash.txt', 'r') as file:
        #         lines = file.readlines()
        #
        #         for line in lines:
        #             zob_hash, evaluation = line.split(',')
        #             if zob_hash == zobrist_hash(self.board):
        #                 return float(evaluation)
        # fen = board.fen()
        # try:
        #     with open(f'EvalCollector\data\{self.board.turn}_{self.get_piece_count(fen)}.txt', 'r') as file:
        #         lines = file.readlines()
        #         for line in lines:
        #             existing_fen, evaluation = line.split(',')
        #             if fen == existing_fen:
        #                 return float(evaluation)
        # except Exception:
        #     return None
        # return None

    def add_evaluation(self, evaluation: float):
        prev_board = self.board.copy()
        move = prev_board.pop()

        pos = Polyglot_Position(
            zobrist_hash(prev_board),
            Polyglot_Move.from_chess_move(prev_board, move),
            abs(int(evaluation * 10)),
            0)

        Polyglot_Writer.write([pos], 'EvalCollector\example.bin')

        # with open('EvalCollector\data\zob_hash.txt', 'a') as file:
        #     line_to_write = f"{zobrist_hash(board=self.board)},{evaluation:.1f}\n"
        #     file.write(line_to_write)
        #     file.close()

        # fen = self.board.fen()
        # address = f'EvalCollector\data\{self.board.turn}_{self.get_piece_count(fen)}.txt'
        # with open(address, 'a') as file:
        #     line_to_write = f"{fen},{evaluation:.1f}\n"
        #     file.write(line_to_write)
        #     file.close()

    @staticmethod
    def get_piece_count(fen):
        piece_count = 0
        for char in fen.split()[0]:
            # can this check be improved with piece letter mapping
            if char.isalpha():
                piece_count += 1
        return piece_count
