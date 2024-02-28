import chess
from PositionEvaluation.position_evaluator import PositionEvaluator
from collections import namedtuple

MoveAndEval = namedtuple('MoveAndEval', ['move', 'evaluation'])


class MinMaxEvaluator:
    position_evaluator = PositionEvaluator()
    DEPTH_TO_USE_BRUTE_FORCE = 3
    INTUITION_SPREAD = 5

    def __init__(self, best_move, alpha, beta, depth, board: chess.Board):
        self.best_move = best_move
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.board = board

    @property
    def use_intuition(self):
        if self.depth <= self.DEPTH_TO_USE_BRUTE_FORCE:
            return False
        else:
            return True

    @staticmethod
    def update_move_list_by_eval(moves_lst: list, worse_eval: float, eval_new_candidate: float,
                                 top_move_candidate: chess.Move, maximizing_side: bool):
        # The move is better than the current worst move
        if (maximizing_side and eval_new_candidate > worse_eval) or (
                not maximizing_side and eval_new_candidate < worse_eval):
            # To have its efficiency improved
            if maximizing_side:
                for move_with_eval in moves_lst:
                    if move_with_eval.evaluation == worse_eval:
                        moves_lst.remove(move_with_eval)
                        moves_lst.append(MoveAndEval(top_move_candidate, eval_new_candidate))
                        break
                return moves_lst, min(moves_lst, key=lambda move_eval_tuple: move_eval_tuple.evaluation).evaluation
            else:
                moves_lst.remove(max(moves_lst, key=lambda move_eval_tuple: move_eval_tuple.evaluation))
                moves_lst.append(MoveAndEval(top_move_candidate, eval_new_candidate))
                return moves_lst, max(moves_lst, key=lambda move_eval_tuple: move_eval_tuple.evaluation).evaluation
        # The move is not better than the current worst move
        return moves_lst, worse_eval

    @staticmethod
    def update_worse_eval(worse_eval: float, candidate_new_eval: float, maximizing_side: bool):
        if (worse_eval in [float('-inf'), float('inf')]) or (maximizing_side and candidate_new_eval < worse_eval) or\
                (not maximizing_side and candidate_new_eval > worse_eval):
            return candidate_new_eval
        return worse_eval

    def get_moves_to_be_considered(self):
        if not self.use_intuition:
            return self.board.legal_moves
        else:
            intuitive_moves = []
            worse_eval = float('-inf') if self.board.turn else float('inf')
            for move in self.board.legal_moves:
                imag_board = self.board.copy()
                imag_board.push(move)
                move_quick_eval = self.position_evaluator.evaluate_position(imag_board)
                if len(intuitive_moves) < self.INTUITION_SPREAD:
                    intuitive_moves.append(MoveAndEval(move, move_quick_eval))
                    worse_eval = self.update_worse_eval(worse_eval=worse_eval, candidate_new_eval=move_quick_eval,
                                                        maximizing_side=self.board.turn)
                    continue

                intuitive_moves, worse_eval = self.update_move_list_by_eval(moves_lst=intuitive_moves,
                                                                            worse_eval=worse_eval,
                                                                            eval_new_candidate=move_quick_eval,
                                                                            top_move_candidate=move,
                                                                            maximizing_side=self.board.turn)

            return [move for move, _ in intuitive_moves]

    def min_max(self):
        if self.depth == 0 or self.board.is_game_over():
            move_eval = self.position_evaluator.evaluate_position(self.board)
            return move_eval

        if self.board.turn:
            for move in self.get_moves_to_be_considered():
                self.board.push(move)
                move_eval = MinMaxEvaluator(self.best_move, self.alpha, self.beta, self.depth - 1, self.board).min_max()
                if move_eval > self.alpha:
                    self.alpha = move_eval
                    self.best_move = move

                    if self.beta <= self.alpha:
                        self.board.pop()
                        return move_eval
                self.board.pop()
            return self.alpha

        if not self.board.turn:
            for move in self.get_moves_to_be_considered():
                self.board.push(move)
                move_eval = MinMaxEvaluator(self.best_move, self.alpha, self.beta, self.depth - 1, self.board).min_max()
                if move_eval < self.beta:
                    self.beta = move_eval
                    self.best_move = move
                    if self.beta <= self.alpha:
                        self.board.pop()
                        return move_eval
                self.board.pop()
            return self.beta


class Engine:
    MAX_DEPTH = 5

    def suggest_move(self, board: chess.Board):
        evaluator = self.create_evaluator(board)
        evaluator.min_max()
        return evaluator.best_move

    def create_evaluator(self, board: chess.Board):
        return MinMaxEvaluator(best_move=None,
                               alpha=float('-inf'),
                               beta=float('inf'),
                               depth=self.MAX_DEPTH,
                               board=board)
