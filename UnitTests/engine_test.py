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


class MinMaxEvaluatorTest(TestCase):
    def setUp(self):
        self.evaluator = MinMaxEvaluator(best_move=None,
                                         alpha=float('-inf'),
                                         beta=float('inf'),
                                         depth=4,
                                         board=chess.Board())

    def test_update_worse_eval_when_new_eval_is_less_and_white_maximizes(self):
        self._run_update_worse_eval_and_assert(worse_eval=2,
                                               candidate_new_eval=1,
                                               maximizing_side=True,
                                               expected_to_return_new_eval=True)

    def test_update_worse_eval_when_new_eval_is_more_and_white_maximizes(self):
        self._run_update_worse_eval_and_assert(worse_eval=2,
                                               candidate_new_eval=3,
                                               maximizing_side=True,
                                               expected_to_return_new_eval=False)

    def test_update_worse_eval_when_new_eval_is_less_and_black_maximizes(self):
        self._run_update_worse_eval_and_assert(worse_eval=2,
                                               candidate_new_eval=1,
                                               maximizing_side=False,
                                               expected_to_return_new_eval=False)

    def test_update_worse_eval_when_new_eval_is_more_and_black_maximizes(self):
        self._run_update_worse_eval_and_assert(worse_eval=2,
                                               candidate_new_eval=3,
                                               maximizing_side=False,
                                               expected_to_return_new_eval=True)

    def _run_update_worse_eval_and_assert(self, worse_eval: float,
                                          candidate_new_eval: float,
                                          maximizing_side: bool,
                                          expected_to_return_new_eval: bool):
        result = self.evaluator.update_worse_eval(worse_eval=worse_eval,
                                                  candidate_new_eval=candidate_new_eval,
                                                  maximizing_side=maximizing_side)
        actual_returned_new_value = result == candidate_new_eval
        self.assertEquals(actual_returned_new_value, expected_to_return_new_eval)
    