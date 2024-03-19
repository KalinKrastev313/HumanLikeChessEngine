from unittest import TestCase
from unittest.mock import patch

from PositionEvaluation.evaluation_functions import *
import chess


class EvaluationFunctionsTest(TestCase):
    def setUp(self):
        self.pawn_at_rank = {
            4: 4,
            5: 5,
            6: 6,
        }
        self.piece_values_dict = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.2,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # We don't want the king to be captured
        }
        self.positional_values_dict = {
            'possible_move': 0.02,
            'one_square_space': 0.01,
            'piece_positioned_in_the_close_center': 0.6,
            'piece_positioned_in_the_broad_center': 0.4
        }

    def test_get_material_evaluation(self):
        expected_evals = [1, 3, 3.2, 5, 9, 0]
        for piece_type in range(1, 7):
            with patch.dict(piece_values_dict, self.piece_values_dict, clear=True):
                self._test_run_get_material_evaluation_and_assert(chess.Piece(piece_type=piece_type, color=True),
                                                                  expected_eval=expected_evals[piece_type - 1])
                self._test_run_get_material_evaluation_and_assert(chess.Piece(piece_type=piece_type, color=False),
                                                                  expected_eval=-expected_evals[piece_type - 1])

    def _test_run_get_material_evaluation_and_assert(self, piece: chess.Piece, expected_eval):
        actual_eval = get_material_evaluation(piece)
        self.assertEquals(actual_eval, expected_eval)

    def test_total_possible_moves_advantage_evaluation_when_white_to_move(self):
        board = chess.Board(fen='rnbqkbnr/ppppppp1/7p/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2')
        board2 = board.copy()
        self._test_run_total_possible_moves_evaluation_and_assert(board2, board, 0.22)

    def test_total_possible_moves_advantage_evaluation_when_black_to_move(self):
        board = chess.Board(fen='rnbqkbnr/ppppppp1/7p/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2')
        board2 = board.copy()
        self._test_run_total_possible_moves_evaluation_and_assert(board2, board, 0.38)

    def _test_run_total_possible_moves_evaluation_and_assert(self, test_board, expected_board, expected_eval):
        with patch.dict(positional_values_dict, self.positional_values_dict, clear=True):
            actual = total_possible_moves_advantage_evaluation(test_board)
        self.assertEquals(test_board, expected_board)
        self.assertEquals(actual, expected_eval)

    def test_pawn_is_advanced_when_pawn_is_white(self):
        piece = chess.Piece(piece_type=1, color=True)
        expected_evals = [0, 0, 0, 0, 4, 5, 6, 0]
        self._test_run_pawn_is_advanced_and_assert(piece, expected_evals)

    def test_pawn_is_advanced_when_pawn_is_black(self):
        piece = chess.Piece(piece_type=1, color=False)
        expected_evals = [0, -6, -5, -4, 0, 0, 0, 0]
        self._test_run_pawn_is_advanced_and_assert(piece, expected_evals)

    def _test_run_pawn_is_advanced_and_assert(self, piece, expected_evals):
        squares = [chess.Square(square) for square in range(0, 64, 8)]
        with patch.dict(pawn_at_rank, self.pawn_at_rank, clear=True):
            for index in range(8):
                actual = pawn_is_advanced(piece, squares[index], chess.Board(fen='rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'))
                self.assertEquals(actual, expected_evals[index])
