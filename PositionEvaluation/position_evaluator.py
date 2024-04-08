from PositionEvaluation.evaluation_functions_mappings import *
from PositionEvaluation.evaluation_functions import *
import chess


class PositionEvaluator:
    def evaluate_position_from_move(self, board: chess.Board, move: chess.Move, current_board_eval: float = None):
        if not current_board_eval:
            board.push(move)
            move_eval = self.evaluate_position(board)
            board.pop()
        else:
            board.push(move)
            if board.is_game_over():
                return self.finished_game_evaluation(board)

            move_eval = 0
            move_eval += total_possible_moves_advantage_evaluation(board)

            board.pop()

            for eval_func in evaluation_functions_mapping:
                move_eval -= evaluation_functions_mapping[eval_func](board.piece_at(move.from_square), move.from_square)
                move_eval += evaluation_functions_mapping[eval_func](board.piece_at(move.from_square), move.to_square)
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    move_eval -= evaluation_functions_mapping[eval_func](board.piece_at(move.to_square), move.to_square)

        return move_eval

    def evaluate_position(self, board: chess.Board):

        if board.is_game_over():
            return self.finished_game_evaluation(board)

        evaluation = 0
        evaluation += total_possible_moves_advantage_evaluation(board)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                evaluation += get_material_evaluation(piece)
                for eval_func in evaluation_functions_mapping:
                    evaluation += evaluation_functions_mapping[eval_func](piece, square)

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
