# from engine import MoveAndEval
from collections import namedtuple

MoveAndEval = namedtuple('MoveAndEval', ['move', 'evaluation'])


class SortedLinkedList:
    def __init__(self, max_length: int, maximizing_side: bool):
        self.max_length = max_length
        self.maximizing_side = maximizing_side
        self.length = 0
        self.min_value = None
        self.max_value = None
        self.smallest_node = None

    def add_move_and_eval(self, move_and_eval: MoveAndEval):
        if not self.smallest_node:
            self.smallest_node = SortedLinkedListNode(move_and_eval)
            self.length = 1
            self.min_value = move_and_eval.evaluation
            self.max_value = move_and_eval.evaluation
        else:
            self._insert_node(move_and_eval=move_and_eval, search_start_node=self.smallest_node)

    def _insert_node(self, move_and_eval: MoveAndEval, search_start_node, previous_node=None):
        if move_and_eval.evaluation <= search_start_node.evaluation:
            if previous_node:
                previous_node.parent_node = SortedLinkedListNode(move_and_eval, search_start_node)
                self._correct_length_right_after_new_node_is_inserted(search_start_node, previous_node)
            elif not previous_node:
                self.smallest_node = SortedLinkedListNode(move_and_eval, search_start_node)
                self.min_value = move_and_eval.evaluation
                self._correct_length_right_after_new_node_is_inserted(search_start_node, None)

        if move_and_eval.evaluation > search_start_node.evaluation:
            if search_start_node.parent_node:
                self._insert_node(move_and_eval, search_start_node.parent_node, search_start_node)
            else:
                search_start_node.parent_node = SortedLinkedListNode(move_and_eval, None)
                self.max_value = move_and_eval.evaluation
                self._correct_length_right_after_new_node_is_inserted(search_start_node, previous_node)

    def _correct_length_right_after_new_node_is_inserted(self, search_start_node, previous_node):
        self.length += 1
        if self.length == self.max_length + 1:
            if self.maximizing_side:
                self.remove_the_smallest_node()
            else:
                if not previous_node:  # minimizing side and smallest_node was added
                    self._remove_the_node_with_no_parent(self.smallest_node.parent_node, self.smallest_node)
                else:  # minimizing side and node was inserted
                    self._remove_the_node_with_no_parent(search_start_node, previous_node.parent_node)

    def remove_the_smallest_node(self):
        if self.length == 0:
            pass
        elif self.length == 1:
            self.empty_the_list()
        elif self.smallest_node.parent_node:
            self.smallest_node = self.smallest_node.parent_node
            self.min_value = self.smallest_node.evaluation
            self.length -= 1

    def remove_biggest_node(self):
        if self.length == 0:
            pass
        elif self.length == 1:
            self.empty_the_list()
        else:
            self._remove_the_node_with_no_parent(self.smallest_node)

    def empty_the_list(self):
        self.length = 0
        self.min_value = None
        self.max_value = None
        self.smallest_node = None

    def _remove_the_node_with_no_parent(self, node, previous_node=None):
        if not node.parent_node:  # last
            previous_node.parent_node = None
            self.length -= 1
            self.max_value = previous_node.evaluation
        elif not node.parent_node.parent_node:  # before the last
            node.parent_node = None
            self.length -= 1
            self.max_value = node.evaluation
        else:  # not before the last or last
            self._remove_the_node_with_no_parent(node.parent_node, node)

    def get_moves(self):
        node = self.smallest_node
        yield node.move
        while node.parent_node:
            yield node.parent_node.move
            node = node.parent_node

    def get_nodes(self):
        node = self.smallest_node
        yield node
        while node.parent_node:
            yield node.parent_node
            node = node.parent_node


class SortedLinkedListNode:
    def __init__(self, move_and_eval: MoveAndEval, parent_node=None):
        self.move_and_eval = move_and_eval
        self.parent_node = parent_node

    @property
    def move(self):
        return self.move_and_eval.move

    @property
    def evaluation(self):
        return self.move_and_eval.evaluation


    # def set_parent_node(self, parent_node):
    #     self.parent_node = parent_node
