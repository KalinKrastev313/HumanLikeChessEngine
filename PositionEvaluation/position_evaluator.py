from PositionEvaluation.evaluation_functions_mappings import *
from PositionEvaluation.evaluation_functions import *
import chess


class PositionEvaluator:

    def evaluate_position(self, board: chess.Board):
        evaluation = self.calculate_evaluation(board)
        return evaluation

    def evaluate_position_from_move(self, board: chess.Board, move: chess.Move):
        board.push(move)
        move_eval = self.evaluate_position(board)
        board.pop()
        return move_eval

    def calculate_evaluation(self, board: chess.Board):

        if board.is_game_over():
            return self.finished_game_evaluation(board)

        evaluation = 0
        evaluation += total_possible_moves_advantage_evaluation(board)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                evaluation += get_material_evaluation(piece)
                for eval_func in evaluation_functions_mapping:
                    evaluation += evaluation_functions_mapping[eval_func](piece, square, board)

        return evaluation

    @staticmethod
    def finished_game_evaluation(board: chess.Board):
        # white is True, black is False, None is draw
        winner = board.outcome().winner
        if winner is True:
            if board.is_checkmate():
                return float(2030 - (len(board.move_stack) // 2))
            return float(2000)
        if winner is False:
            if board.is_checkmate():
                return -float(2030 - (len(board.move_stack) // 2))
            return -float(2000)
        if winner is None:
            return float(0)
