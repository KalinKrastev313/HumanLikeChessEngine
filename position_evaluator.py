import chess

positional_values_dict = {
    'possible_move': 0.1,
    'one_square_space': 1
}


def total_possible_moves_advantage_evaluation(board: chess.Board):
    side_to_move = board.turn
    number_of_possible_moves = len(list(board.legal_moves))
    board.push(chess.Move.null())
    other_side_possible_moves = len(list(board.legal_moves))
    evaluation = (number_of_possible_moves - other_side_possible_moves) * positional_values_dict['possible_move']
    if side_to_move:
        return evaluation
    return -evaluation


def pieces_are_forward(board: chess.Board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color:
                evaluation += chess.square_rank(square)
            else:
                evaluation += chess.square_rank(square) - 7

    return evaluation * positional_values_dict['one_square_space']


positional_evaluation_functions_mapping = {
    'amount_of_possible_moves': total_possible_moves_advantage_evaluation,
    'space_advantage': pieces_are_forward
    # 'pieces_in_center': 5,
    # 'has_knight': 5,
    # 'has_bishop': 5,
    # 'has_rook': 5,
    # 'has_queen': 5,
}

piece_values_dict = {
                    chess.PAWN: 1,
                    chess.KNIGHT: 3,
                    chess.BISHOP: 3.2,
                    chess.ROOK: 5,
                    chess.QUEEN: 9,
                    chess.KING: 0  # We don't want the king to be captured
                }


class MaterialEvaluator:
    piece_values_dict = piece_values_dict

    def get_material_evaluation(self, board: chess.Board):
        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = self.piece_values_dict[piece.piece_type]

                evaluation += value if piece.color == chess.WHITE else -value

        return evaluation


class PositionalEvaluator:
    POSITIONAL_EVALUATION_FUNCS_MAPPING = positional_evaluation_functions_mapping

    def get_positional_evaluation(self, board: chess.Board):
        evaluation = 0
        for func in self.POSITIONAL_EVALUATION_FUNCS_MAPPING:
            evaluation += self.POSITIONAL_EVALUATION_FUNCS_MAPPING[func](board.copy())

        return evaluation


class PositionEvaluator:
    MATERIAL_EVALUATOR = MaterialEvaluator()
    POSITIONAL_EVALUATOR = PositionalEvaluator()

    def evaluate_position(self, board: chess.Board):
        if board.is_game_over():
            return self.finished_game_evaluation(board)

        evaluation = 0
        evaluation += self.MATERIAL_EVALUATOR.get_material_evaluation(board)
        evaluation += self.POSITIONAL_EVALUATOR.get_positional_evaluation(board)

        return evaluation

    @staticmethod
    def finished_game_evaluation(board: chess.Board):
        # white is True, black is False, None is draw
        winner = board.outcome().winner
        if winner is True:
            return float(2000)
        if winner is False:
            return float(-2000)
        if winner is None:
            return float(0)


