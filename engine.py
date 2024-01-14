import chess
from position_evaluator import PositionEvaluator


class MinMaxEvaluator:
    position_evaluator = PositionEvaluator()

    def __init__(self, best_move, alpha, beta, depth, board: chess.Board):
        self.best_move = best_move
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.board = board

    def min_max(self):
        if self.depth == 0 or self.board.is_game_over():
            move_eval = self.position_evaluator.evaluate_position(self.board)
            return move_eval

        if self.board.turn:
            for move in self.board.legal_moves:
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
            for move in self.board.legal_moves:
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
    MAX_DEPTH = 4

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
