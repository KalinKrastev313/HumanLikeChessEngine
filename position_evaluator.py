from EvalCollector.evaluation_collector import EvalCollector
from evaluation_functions_mappings import *
from evaluation_functions import *
import chess


class PositionEvaluator:
    USE_PREV_EVAL = False
    EVAL_COLLECTOR = EvalCollector

    def evaluate_position(self, board: chess.Board):
        evaluation = None
        if self.USE_PREV_EVAL:
            evaluation = self.check_for_prev_move_eval(board)

        if evaluation and self.USE_PREV_EVAL:
            return evaluation
        else:
            evaluation = self.calculate_evaluation(board)

        self.collect_eval(evaluation, board)
        return evaluation

    def check_for_prev_move_eval(self, board: chess.Board):
        if self.USE_PREV_EVAL:
            return self.EVAL_COLLECTOR(board=board).check_for_prev_eval()
        else:
            return None

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

    def collect_eval(self, evaluation: float, board: chess.Board):
        if self.USE_PREV_EVAL:
            self.EVAL_COLLECTOR(board).add_evaluation(evaluation)

    @staticmethod
    def finished_game_evaluation(board: chess.Board):
        # white is True, black is False, None is draw
        winner = board.outcome().winner
        if winner is True:
            return float(2000)
        if winner is False:
            return float(-2000)
        if winner is None:
            return float(0)
