import chess

piece_values_dict = {
                    chess.PAWN: 1,
                    chess.KNIGHT: 3,
                    chess.BISHOP: 3.2,
                    chess.ROOK: 5,
                    chess.QUEEN: 9,
                    chess.KING: 0  # We don't want the king to be captured
                }

positional_values_dict = {
    'possible_move': 0.02,
    'one_square_space': 0.01,
    'piece_positioned_in_the_close_center': 0.6,
    'piece_positioned_in_the_broad_center': 0.4
}

pawn_at_rank = {
    #  On python chess the ranks are from 0 to 7. We trace only for the ranks further on the board where a pawn can be.
    4: 4,  # white pawn at 5th rank or black pawn at fourth rank
    5: 5,  # white pawn at 6th rank or black pawn at third rank
    6: 6,  # white pawn at 7th rank or black pawn at second rank
}

close_central_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
broad_central_squares = [chess.C3, chess.D3, chess.E3, chess.F3,
                         chess.C4, chess.F4, chess.C5, chess.F5,
                         chess.C6, chess.D6, chess.E6, chess.F6]
