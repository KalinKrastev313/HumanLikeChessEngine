from unittest.mock import patch
import chess

import PositionEvaluation.position_evaluator
from PositionEvaluation.position_evaluator import PositionEvaluator
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

    def test_get_moves_to_be_considered_returns_all_possible_moves_when_intuition_not_used(self):
        with patch.object(MinMaxEvaluator, 'use_intuition', False) as use_intuition:
            moves_to_be_considered = self.evaluator.get_moves_to_be_considered()

        self.assertEquals(list(moves_to_be_considered), list(self.evaluator.board.legal_moves))

    def test_moves_to_be_considered_when_intuition_used_and_possible_moves_are_less_than_intuition_spread(self):
        self.evaluator.INTUITION_SPREAD = 5

        actual_moves_to_be_considered = self._test_run_get_moves_to_be_considered(len_legal_moves_found=3,
                                                                                  mocked_evaluations=[1, 2, 3])
        expected_moves_to_be_considered = [chess.Move.from_uci('c4f7'),
                                           chess.Move.from_uci('c4e6'),
                                           chess.Move.from_uci('c4a6')]
        self.assertEquals(actual_moves_to_be_considered, expected_moves_to_be_considered)

    def test_moves_to_be_considered_when_intuition_used_and_possible_moves_are_more_than_intuition_spread(self):
        self.evaluator.INTUITION_SPREAD = 3

        actual_moves_to_be_considered = self._test_run_get_moves_to_be_considered(len_legal_moves_found=4,
                                                                                  mocked_evaluations=[1, 2, 3, 4])
        expected_moves_to_be_considered = [chess.Move.from_uci('c4e6'),
                                           chess.Move.from_uci('c4a6'),
                                           chess.Move.from_uci('c4d5')]
        self.assertEquals(actual_moves_to_be_considered, expected_moves_to_be_considered)

    def test_moves_to_be_considered_with_intuition_small_intuition_spread_and_minimizing_side(self):
        self.evaluator.INTUITION_SPREAD = 3
        self.evaluator.board.turn = False

        actual_moves_to_be_considered = self._test_run_get_moves_to_be_considered(len_legal_moves_found=4,
                                                                                  mocked_evaluations=[1, 2, 3, 4])
        expected_moves_to_be_considered = [chess.Move.from_uci('c4f7'),
                                           chess.Move.from_uci('c4e6'),
                                           chess.Move.from_uci('c4a6')]
        self.assertEquals(actual_moves_to_be_considered, expected_moves_to_be_considered)

    def _test_run_get_moves_to_be_considered(self, len_legal_moves_found, mocked_evaluations):
        with patch.object(chess.Board, 'legal_moves', self._test_get_list_of_moves()[:len_legal_moves_found]) as legal_move_generator:
            with patch.object(PositionEvaluator, 'evaluate_position_from_move') as move_evaluations:
                move_evaluations.side_effect = mocked_evaluations
                return self.evaluator.get_moves_to_be_considered()

    @staticmethod
    def _test_get_list_of_moves():
        specific_board = chess.Board(fen='r2qkbnr/ppp2pp1/2np3p/4p2b/2BPP3/2N2N1P/PPP2PP1/R1BQK2R w KQkq - 1 7')
        return list(specific_board.legal_moves)

    def test_min_max_branch_stops_when_game_is_drawn_due_to_repetition_and_returns_eval(self):
        test_board = chess.Board()
        moves_to_be_repeated = [chess.Move.from_uci('g1f3'),
                                chess.Move.from_uci('g8f6'),
                                chess.Move.from_uci('f3g1'),
                                chess.Move.from_uci('f6g8')]

        #  python chess :func: outcome doc detects fivefold repetition, but threefold is slower to detect
        for _ in range(5):
            for move in moves_to_be_repeated:
                test_board.push(move)

        self.evaluator.board = test_board
        position_eval = self.evaluator.min_max()
        self.assertEquals(position_eval, 0)

    def test_min_max_branch_stops_when_game_is_drawn_due_to_stalemate_and_returns_eval(self):
        self.evaluator.board = chess.Board(fen='k7/1R6/2K5/8/8/8/8/8 b - - 0 1')
        position_eval = self.evaluator.min_max()
        self.assertEquals(position_eval, 0)

    def test_min_max_stops_when_one_side_checkmates_the_other(self):
        self.evaluator.board = chess.Board(fen='k1R5/8/1K6/8/8/8/8/8 b - - 0 1')
        self.assertGreaterEqual(self.evaluator.min_max(), 200)

        self.evaluator.board = chess.Board(fen='K1r5/8/1k6/8/8/8/8/8 w - - 0 1')
        self.assertLessEqual(self.evaluator.min_max(), -200)

    def test_min_max_branch_stops_when_maximum_depth_is_reached(self):
        self.evaluator.depth = 0
        with patch.object(self.evaluator.position_evaluator, 'evaluate_position') as position_evaluator:
            position_evaluator.return_value = 2
            actual = self.evaluator.min_max()

        self.assertEquals(actual, 2)

    def test_white_finds_better_move_but_not_enough_to_prune(self):
        self.evaluator.alpha = 2
        self._test_execute_min_max_then_assert(expected_min_max_eval=4,
                                               expected_best_move=chess.Move.from_uci('d2d4'))

    def test_white_finds_better_move_enough_to_prune(self):
        self.evaluator.alpha = 2
        self.evaluator.beta = 3
        self._test_execute_min_max_then_assert(expected_min_max_eval=3,
                                               expected_best_move=chess.Move.from_uci('e2e4'))

    def test_white_doesnt_find_a_better_move(self):
        self.evaluator.alpha = 5
        self.evaluator.best_move = chess.Move.from_uci('f2f4')
        self._test_execute_min_max_then_assert(expected_min_max_eval=5,
                                               expected_best_move=chess.Move.from_uci('f2f4'))

    def test_black_finds_a_better_move_but_not_enough_to_prune(self):
        self.evaluator.beta = 5
        self.evaluator.board.turn = False
        self._test_execute_min_max_then_assert(expected_min_max_eval=3,
                                               expected_best_move=chess.Move.from_uci('e2e4'))

    def test_black_finds_a_better_move_enough_to_prune(self):
        self.evaluator.beta = 5
        self.evaluator.alpha = 4
        self.evaluator.board.turn = False
        self._test_execute_min_max_then_assert(expected_min_max_eval=3,
                                               expected_best_move=chess.Move.from_uci('e2e4'),
                                               move_evals_returns=[3, 2])

    def test_black_doesnt_find_a_better_move(self):
        self.evaluator.beta = 2
        self.evaluator.best_move = chess.Move.from_uci('g8f6')
        self.evaluator.board.turn = False
        self._test_execute_min_max_then_assert(expected_min_max_eval=2,
                                               expected_best_move=chess.Move.from_uci('g8f6'))

    def _test_execute_min_max_then_assert(self, expected_min_max_eval, expected_best_move, move_evals_returns=None ):
        with patch.object(self.evaluator, 'get_moves_to_be_considered') as move_generator:
            move_generator.return_value = [chess.Move.from_uci('e2e4'),
                                           chess.Move.from_uci('d2d4')]
            with patch.object(self.evaluator, 'create_a_branch_and_calculate_its_evaluation') as get_move_eval:
                get_move_eval.side_effect = [3, 4] if not move_evals_returns else move_evals_returns
                new_eval = self.evaluator.min_max()

        self.assertEquals(new_eval, expected_min_max_eval)
        self.assertEquals(self.evaluator.best_move, expected_best_move)
