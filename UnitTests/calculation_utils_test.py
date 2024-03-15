import chess

from calculation_utils import SortedLinkedList

from unittest import TestCase

from engine import MoveAndEval


class SortedLinkedListTest(TestCase):
    def _test_assert_linked_list_attributes(self, linked_list,
                                            expected_length,
                                            expected_min_value,
                                            expected_max_value,
                                            expected_smallest_node_move,
                                            expected_smallest_node_evaluation):
        self.assertEquals(linked_list.length, expected_length)
        self.assertEquals(linked_list.min_value, expected_min_value)
        self.assertEquals(linked_list.max_value, expected_max_value)
        self.assertEquals(linked_list.smallest_node.move, expected_smallest_node_move)
        self.assertEquals(linked_list.smallest_node.evaluation, expected_smallest_node_evaluation)

    def _test_assert_linked_list_is_empty(self, linked_list):
        self.assertEquals(linked_list.length, 0)
        self.assertEquals(linked_list.min_value, None)
        self.assertEquals(linked_list.max_value, None)
        self.assertEquals(linked_list.smallest_node, None)

    def test_add_node_when_the_list_is_empty(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=1,
                                                 expected_min_value=5,
                                                 expected_max_value=5,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_add_node_when_value_bigger_than_max_value_and_space_left(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 7))
        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=5,
                                                 expected_max_value=7,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_add_node_when_value_between_existing_nodes_values_and_space_left(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 7))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 6))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=3,
                                                 expected_min_value=5,
                                                 expected_max_value=7,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_add_node_when_value_smaller_than_min_value_and_space_left(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 7))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 4))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=3,
                                                 expected_min_value=4,
                                                 expected_max_value=7,
                                                 expected_smallest_node_move=chess.Move.from_uci('c2c4'),
                                                 expected_smallest_node_evaluation=4)

    def test_add_node_smaller_than_last_node_when_maximizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=1, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=1,
                                                 expected_min_value=5,
                                                 expected_max_value=5,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_add_node_smaller_than_last_node_when_minimizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=1, maximizing_side=False)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=1,
                                                 expected_min_value=4,
                                                 expected_max_value=4,
                                                 expected_smallest_node_move=chess.Move.from_uci('d2d4'),
                                                 expected_smallest_node_evaluation=4)

    def test_add_node_bigger_than_all_nodes_when_maximizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 7))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=5,
                                                 expected_max_value=7,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_add_node_bigger_than_all_nodes_when_minimizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=False)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 7))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=4,
                                                 expected_max_value=5,
                                                 expected_smallest_node_move=chess.Move.from_uci('d2d4'),
                                                 expected_smallest_node_evaluation=4)

    def test_add_node_between_other_nodes_by_size_when_maximizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 4.5))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=4.5,
                                                 expected_max_value=5,
                                                 expected_smallest_node_move=chess.Move.from_uci('c2c4'),
                                                 expected_smallest_node_evaluation=4.5)

    def test_add_node_between_other_nodes_by_size_when_minimizing_side_and_no_space(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=False)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 4.5))

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=4,
                                                 expected_max_value=4.5,
                                                 expected_smallest_node_move=chess.Move.from_uci('d2d4'),
                                                 expected_smallest_node_evaluation=4)

    def test_remove_the_smallest_node_when_there_are_several_nodes(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2d4'), 4))

        linked_list.remove_the_smallest_node()

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=1,
                                                 expected_min_value=5,
                                                 expected_max_value=5,
                                                 expected_smallest_node_move=chess.Move.from_uci('e2e4'),
                                                 expected_smallest_node_evaluation=5)

    def test_remove_the_smallest_node_when_there_is_only_one_node(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        linked_list.remove_the_smallest_node()

        self._test_assert_linked_list_is_empty(linked_list)

    def test_remove_the_smallest_node_when_there_are_no_nodes(self):
        linked_list = SortedLinkedList(max_length=2, maximizing_side=True)

        linked_list.remove_the_smallest_node()

        self._test_assert_linked_list_is_empty(linked_list)

    def test_remove_the_biggest_node_when_there_are_no_nodes(self):
        linked_list = SortedLinkedList(max_length=1, maximizing_side=True)

        linked_list.remove_biggest_node()

        self._test_assert_linked_list_is_empty(linked_list)

    def test_remove_the_biggest_node_when_there_is_only_one_node(self):
        linked_list = SortedLinkedList(max_length=1, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))

        linked_list.remove_biggest_node()

        self._test_assert_linked_list_is_empty(linked_list)

    def test_remove_the_biggest_node_when_two_or_more_nodes(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('e2e4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('d2e4'), 4))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('c2c4'), 3))

        linked_list.remove_biggest_node()

        self._test_assert_linked_list_attributes(linked_list=linked_list,
                                                 expected_length=2,
                                                 expected_min_value=3,
                                                 expected_max_value=4,
                                                 expected_smallest_node_move=chess.Move.from_uci('c2c4'),
                                                 expected_smallest_node_evaluation=3)

    def test_empty_the_list(self):
        linked_list = SortedLinkedList(max_length=3, maximizing_side=True)
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('b2b4'), 5))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('a2a4'), 4))
        linked_list.add_move_and_eval(MoveAndEval(chess.Move.from_uci('f2f4'), 3))

        linked_list.empty_the_list()

        self._test_assert_linked_list_is_empty(linked_list)
