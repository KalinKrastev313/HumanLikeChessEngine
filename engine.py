import chess
from PositionEvaluation.position_evaluator import PositionEvaluator

from calculation_utils import SortedLinkedList, MoveAndEval
from chess.polyglot import MemoryMappedReader


class MinMaxEvaluator:
    position_evaluator = PositionEvaluator()
    DEPTH_TO_USE_BRUTE_FORCE = 3
    INTUITION_SPREAD = 10

    def __init__(self, best_move, alpha, beta, depth, board: chess.Board, board_static_eval=None):
        self.best_move = best_move
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.board = board
        self.board_static_eval = board_static_eval

    @property
    def use_intuition(self):
        # return False
        if self.depth <= self.DEPTH_TO_USE_BRUTE_FORCE:
            return False
        else:
            return True

    def get_moves_to_be_considered(self):
        if not self.use_intuition:
            return self.board.legal_moves
        else:
            intuitive_moves = SortedLinkedList(max_length=self.INTUITION_SPREAD, maximizing_side=self.board.turn)

            current_board_quick_eval = self.board_static_eval if self.board_static_eval else self.position_evaluator.evaluate_position(self.board)

            for move in self.board.legal_moves:
                move_quick_eval = self.position_evaluator.evaluate_position_statically_from_move(self.board, move, current_board_quick_eval)
                intuitive_moves.add_move_and_eval(MoveAndEval(move, move_quick_eval))

            return intuitive_moves.get_moves()

    def create_a_branch_and_calculate_its_evaluation(self, move: chess.Move):
        self.board.push(move)
        move_eval = MinMaxEvaluator(self.best_move, self.alpha, self.beta, self.depth - 1, self.board).min_max()
        self.board.pop()
        return move_eval

    def min_max(self):
        if self.depth == 0 or self.board.is_game_over():
            move_eval = self.position_evaluator.evaluate_position(self.board, dynamic_evaluation=True)
            return move_eval

        if self.board.turn:
            for move in self.get_moves_to_be_considered():
                move_eval = self.create_a_branch_and_calculate_its_evaluation(move)
                if move_eval > self.alpha:
                    self.alpha = move_eval
                    self.best_move = move
                    if self.beta <= self.alpha:
                        return move_eval
            return self.alpha

        if not self.board.turn:
            for move in self.get_moves_to_be_considered():
                move_eval = self.create_a_branch_and_calculate_its_evaluation(move)
                if move_eval < self.beta:
                    self.beta = move_eval
                    self.best_move = move
                    if self.beta <= self.alpha:
                        return move_eval
            return self.beta


class Engine:
    USE_LAST_EVAL = True
    MAX_DEPTH = 5
    LAST_EVAL = None
    USE_OPENING_BOOKS = False

    def __init__(self, opening_book_white=None, opening_book_black=None):
        self.opening_book_white = opening_book_white
        self.opening_book_black = opening_book_black

    def read_opening_book(self, board: chess.Board):
        if board.turn and self.opening_book_white:
            return self.opening_book_white.get(board)
        elif self.opening_book_black:
            return self.opening_book_black.get(board)
        else:
            return None

    def suggest_move(self, board: chess.Board):
        if self.USE_OPENING_BOOKS:
            book_move = self.read_opening_book(board)
            if book_move:
                return book_move.move

        evaluator = self.create_evaluator(board)
        evaluator.min_max()
        if self.USE_LAST_EVAL:
            self.LAST_EVAL = evaluator.alpha if board.turn else evaluator.beta
        return evaluator.best_move

    def create_evaluator(self, board: chess.Board):
        evaluator = MinMaxEvaluator(best_move=None,
                                    alpha=float('-inf'),
                                    beta=float('inf'),
                                    depth=self.MAX_DEPTH,
                                    board=board)
        if self.USE_LAST_EVAL:
            if self.LAST_EVAL and self.LAST_EVAL not in range(-5, 5):
                evaluator.INTUITION_SPREAD = 5 + abs(self.LAST_EVAL) // 2
            else:
                evaluator.INTUITION_SPREAD = 5
        return evaluator
