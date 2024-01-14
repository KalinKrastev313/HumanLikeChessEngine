from unittest.mock import patch
import chess
from engine import Engine, MinMaxEvaluator

from unittest import TestCase


class EngineTest(TestCase):
    def test_create_evaluator(self):
        board = chess.Board(fen='2b1k2r/1p1n3p/6p1/1P1QPp2/8/2P5/1b1P1KPP/7r b k - 0 21')
        engine = Engine()

        evaluator = engine.create_evaluator(board)

        self.assertEquals(evaluator.best_move, None)
        self.assertEquals(evaluator.alpha, float('-inf'))
        self.assertEquals(evaluator.beta, float('inf'))
        self.assertEquals(evaluator.depth, engine.MAX_DEPTH)
        self.assertEquals(evaluator.board, board)

    def test_suggest_move_executes_min_max_algorithm(self):
        engine = Engine()
        with patch.object(MinMaxEvaluator, 'min_max') as min_max:
            engine.suggest_move(chess.Board(fen='2b1k2r/1p1n3p/6p1/1P1QPp2/8/2P5/1b1P1KPP/7r b k - 0 21'))

        self.assertEquals(min_max.call_count, True)
