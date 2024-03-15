import chess

from definitions_and_factor_weights import *


def get_material_evaluation(piece: chess):
    value = piece_values_dict[piece.piece_type]
    return value if piece.color == chess.WHITE else -value


def total_possible_moves_advantage_evaluation(board: chess.Board):
    side_to_move = board.turn
    number_of_possible_moves = len(list(board.legal_moves))
    board.push(chess.Move.null())
    other_side_possible_moves = len(list(board.legal_moves))
    evaluation = (number_of_possible_moves - other_side_possible_moves) * positional_values_dict['possible_move']
    board.pop()
    if side_to_move:
        return evaluation
    return -evaluation


def piece_is_forward(piece: chess.Piece, square: chess.Square, board: chess.Board):
    if piece.color:
        return chess.square_rank(square) * positional_values_dict['one_square_space']
    else:
        return (chess.square_rank(square) - 7) * positional_values_dict['one_square_space']


def piece_in_the_center(piece: chess.Piece, square: chess.Square, board: chess.Board):
    if square in close_central_squares:
        if piece.color:
            return positional_values_dict['piece_positioned_in_the_close_center']
        else:
            return - positional_values_dict['piece_positioned_in_the_close_center']
    elif square in broad_central_squares:
        if piece.color:
            return positional_values_dict['piece_positioned_in_the_broad_center']
        else:
            return - positional_values_dict['piece_positioned_in_the_broad_center']
    return 0


def pawn_is_advanced(piece: chess.Piece, square: chess.Square, board: chess.Board):
    if piece.piece_type == 1:
        if piece.color and chess.square_rank(square) in range(4, 7):
            return pawn_at_rank[chess.square_rank(square)]
        elif not piece.color and chess.square_rank(square) in range(1, 4):
            return -pawn_at_rank[7 - chess.square_rank(square)]
    return 0


def get_attackers_defenders_power_disbalance(defender: chess.Piece, square: chess.Square, board: chess.Board):
    evaluation = 0
    attackers = board.attackers(not defender.color, square)
    for attacker_square in attackers:
        attacker = board.piece_at(attacker_square)
        if defender.color:
            evaluation += attacker_attacks_defender_weights_mapping[attacker.piece_type - 1][defender.piece_type - 1]
        else:
            evaluation -= attacker_attacks_defender_weights_mapping[attacker.piece_type - 1][defender.piece_type - 1]
    return evaluation

