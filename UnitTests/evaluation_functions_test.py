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
