from PositionEvaluation.evaluation_functions import piece_is_forward, piece_in_the_center


evaluation_functions_mapping = {
    'space_advantage': piece_is_forward,
    'pieces_in_center': piece_in_the_center
    # 'has_knight': 5,
    # 'has_bishop': 5,
    # 'has_rook': 5,
    # 'has_queen': 5,
}
