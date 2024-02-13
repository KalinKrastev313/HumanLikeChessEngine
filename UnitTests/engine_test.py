from unittest.mock import patch
import chess
from engine import Engine, MinMaxEvaluator, MoveAndEval

from unittest import TestCase


class EngineTest(TestCase):
    def setUp(self):
        self.engine = Engine()
        self.engine.MAX_DEPTH = 1

    def test_create_evaluator(self):
        board = chess.Board(fen='2b1k2r/1p1n3p/6p1/1P1QPp2/8/2P5/1b1P1KPP/7r b k - 0 21')

        evaluator = self.engine.create_evaluator(board)

        self.assertEquals(evaluator.best_move, None)
        self.assertEquals(evaluator.alpha, float('-inf'))
        self.assertEquals(evaluator.beta, float('inf'))
        self.assertEquals(evaluator.depth, self.engine.MAX_DEPTH)
        self.assertEquals(evaluator.board, board)

    def test_suggest_move_executes_min_max_algorithm(self):
        with patch.object(MinMaxEvaluator, 'min_max') as min_max:
            self.engine.suggest_move(chess.Board(fen='2b1k2r/1p1n3p/6p1/1P1QPp2/8/2P5/1b1P1KPP/7r b k - 0 21'))

        self.assertEquals(min_max.call_count, True)

    def test_suggest_move_returns_a_move(self):
        board = chess.Board()

        suggested_move = self.engine.suggest_move(board)
        self.assertIsInstance(suggested_move, chess.Move)

    def test_suggest_move_finds_mate_in_one(self):
        board = chess.Board(fen='3k4/8/3K4/5R2/8/8/8/8 w - - 0 1')

        suggested_move = self.engine.suggest_move(board)
        self.assertEquals(suggested_move, chess.Move.from_uci('f5f8'))

    def test_suggest_move_finds_mate_in_two(self):
        board = chess.Board(fen='4k3/8/3K4/6R1/8/8/8/8 w - - 0 1')
        self.engine.MAX_DEPTH = 3

        suggested_move = self.engine.suggest_move(board)
        self.assertEquals(suggested_move, chess.Move.from_uci('g5f5'))


class MinMaxEvaluatorTest(TestCase):
    def setUp(self):
        self.evaluator = MinMaxEvaluator(best_move=None,
                                         alpha=float('-inf'),
                                         beta=float('inf'),
                                         depth=4,
                                         board=chess.Board())

    def test_brute_force_at_low_depth_left(self):
        self.evaluator.depth = 3
        use_intuition = self.evaluator.use_intuition

        self.assertEquals(use_intuition, False)

    def test_use_intuition_when_high_depth_left(self):
        use_intuition = self.evaluator.use_intuition

        self.assertEquals(use_intuition, True)

    def test_update_move_list_by_eval_when_new_move_is_worse_for_max_side_and_max_side(self):
        moves_lst, worst_eval = self._test_get_moves_lst_and_its_worst_eval()

        new_moves_lst, worst_eval = self.evaluator.update_move_list_by_eval(moves_lst=moves_lst,
                                                                            worse_eval=worst_eval,
                                                                            eval_new_candidate=-1,
                                                                            top_move_candidate=chess.Move.from_uci('a2a3'),
                                                                            maximizing_side=True)

        expected_moves_lst, expected_worst_eval = self._test_get_moves_lst_and_its_worst_eval()

        self.assertEquals(new_moves_lst, expected_moves_lst)
        self.assertEquals(worst_eval, expected_worst_eval)

    def test_update_move_list_by_eval_when_new_move_is_worse_for_max_side_and_min_side(self):
        moves_lst, worst_eval = self._test_get_moves_lst_and_its_worst_eval()

        new_moves_lst, worst_eval = self.evaluator.update_move_list_by_eval(moves_lst=moves_lst,
                                                                            worse_eval=worst_eval,
                                                                            eval_new_candidate=-1,
                                                                            top_move_candidate=chess.Move.from_uci('a2a3'),
                                                                            maximizing_side=False)

        expected_moves_lst = [MoveAndEval(chess.Move.from_uci('d2d4'), 1),
                              MoveAndEval(chess.Move.from_uci('f2f4'), 0),
                              MoveAndEval(chess.Move.from_uci('a2a3'), -1)]
        expected_worst_eval = 1
        self.assertCountEqual(new_moves_lst, expected_moves_lst)
        self.assertEquals(worst_eval, expected_worst_eval)

    def test_update_move_list_by_eval_when_new_move_is_better_for_max_side_and_max_side(self):
        moves_lst, worst_eval = self._test_get_moves_lst_and_its_worst_eval()

        new_moves_lst, worst_eval = self.evaluator.update_move_list_by_eval(moves_lst=moves_lst,
                                                                            worse_eval=worst_eval,
                                                                            eval_new_candidate=2.5,
                                                                            top_move_candidate=chess.Move.from_uci('g1f3'),
                                                                            maximizing_side=True)

        expected_moves_lst = [MoveAndEval(chess.Move.from_uci('g1f3'), 2.5),
                              MoveAndEval(chess.Move.from_uci('e1e4'), 2),
                              MoveAndEval(chess.Move.from_uci('d2d4'), 1)]
        expected_worst_eval = 1

        self.assertCountEqual(new_moves_lst, expected_moves_lst)
        self.assertEquals(worst_eval, expected_worst_eval)

    def test_update_move_list_by_eval_when_new_move_is_better_for_max_side_and_min_side(self):
        moves_lst, worst_eval = self._test_get_moves_lst_and_its_worst_eval()

        new_moves_lst, worst_eval = self.evaluator.update_move_list_by_eval(moves_lst=moves_lst,
                                                                            worse_eval=worst_eval,
                                                                            eval_new_candidate=-1,
                                                                            top_move_candidate=chess.Move.from_uci('g1f3'),
                                                                            maximizing_side=False)

        expected_moves_lst = moves_lst
        expected_worst_eval = 1
        self.assertCountEqual(new_moves_lst, expected_moves_lst)
        self.assertEquals(worst_eval, expected_worst_eval)

    @staticmethod
    def _test_get_moves_lst_and_its_worst_eval():
        return [MoveAndEval(chess.Move.from_uci('e1e4'), 2),
                MoveAndEval(chess.Move.from_uci('d2d4'), 1),
                MoveAndEval(chess.Move.from_uci('f2f4'), 0)], 0

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
    