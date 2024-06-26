from unittest import TestCase
from unittest.mock import patch

from PositionEvaluation.evaluation_functions import *
import chess


class EvaluationFunctionsTest(TestCase):
    def setUp(self):
        self.board = chess.Board(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
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

    def test_piece_is_forward_when_it_is_white(self):
        self._test_run_piece_is_forward_and_assert(piece=chess.Piece(piece_type=1, color=True),
                                                   expected_values=[0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07])

    def test_piece_is_forward_when_it_is_black(self):
        self._test_run_piece_is_forward_and_assert(piece=chess.Piece(piece_type=1, color=False),
                                                   expected_values=[-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0])

    def _test_run_piece_is_forward_and_assert(self, piece, expected_values):
        with patch.dict(positional_values_dict, self.positional_values_dict, clear=True):
            for square in range(0, 64, 8):
                actual_value = piece_is_forward(piece, chess.Square(square))
                self.assertEquals(actual_value, expected_values[square // 8])

    def test_piece_in_the_center_when_in_the_close_center_and_white(self):
        self._test_run_piece_in_the_center_and_assert(piece=chess.Piece(piece_type=1, color=True),
                                                      square=chess.Square(28),
                                                      expected_value=0.6)

    def test_piece_in_the_center_when_in_the_broad_center_and_white(self):
        self._test_run_piece_in_the_center_and_assert(piece=chess.Piece(piece_type=1, color=True),
                                                      square=chess.Square(20),
                                                      expected_value=0.4)

    def test_piece_in_the_center_when_in_the_close_center_and_black(self):
        self._test_run_piece_in_the_center_and_assert(piece=chess.Piece(piece_type=1, color=False),
                                                      square=chess.Square(28),
                                                      expected_value=-0.6)

    def test_piece_in_the_center_when_in_the_broad_center_and_black(self):
        self._test_run_piece_in_the_center_and_assert(piece=chess.Piece(piece_type=1, color=False),
                                                      square=chess.Square(20),
                                                      expected_value=-0.4)

    def test_piece_in_the_center_when_not_in_center_and_black(self):
        self._test_run_piece_in_the_center_and_assert(piece=chess.Piece(piece_type=1, color=False),
                                                      square=chess.Square(4),
                                                      expected_value=0)

    def _test_run_piece_in_the_center_and_assert(self, piece, square, expected_value):
        with patch.dict(positional_values_dict, self.positional_values_dict, clear=True):
            actual_value = piece_in_the_center(piece, square)
            self.assertEquals(actual_value, expected_value)

    def test_pawn_is_advanced_when_pawn_is_white(self):
        self._test_run_pawn_is_advanced_and_assert(piece=chess.Piece(piece_type=1, color=True),
                                                   expected_evals=[0, 0, 0, 0, 4, 5, 6, 0])

    def test_pawn_is_advanced_when_pawn_is_black(self):
        self._test_run_pawn_is_advanced_and_assert(piece=chess.Piece(piece_type=1, color=False),
                                                   expected_evals=[0, -6, -5, -4, 0, 0, 0, 0])

    def _test_run_pawn_is_advanced_and_assert(self, piece, expected_evals):
        squares = [chess.Square(square) for square in range(0, 64, 8)]
        with patch.dict(pawn_at_rank, self.pawn_at_rank, clear=True):
            for index in range(8):
                actual = pawn_is_advanced(piece, squares[index])
                self.assertEquals(actual, expected_evals[index])
