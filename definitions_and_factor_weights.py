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


attacker_attacks_defender_weights_mapping = ((0.5,  # pawn attacking pawn
                                              1.5,  # pawn attacking knight
                                              1.6,  # pawn attacking bishop
                                              2.5,  # pawn attacking rook
                                              4.5,  # pawn attacking queen
                                              20),  # pawn attacking king
                                            (0.4,  # knight attacking pawn
                                              1.4,  # knight attacking knight
                                              1.6,  # knight attacking bishop
                                              2.4,  # knight attacking rook
                                              4.5,  # knight attacking queen
                                                20),  # knight attacking king
                                            (0.4,  # bishop attacking pawn
                                              2,  # bishop attacking knight
                                              3,  # bishop attacking bishop
                                              4,  # bishop attacking rook
                                              7,  # bishop attacking queen
                                             20),  # bishop attacking king
                                            (0.2,  # rook attacking pawn
                                              0.4,  # rook attacking knight
                                              0.4,  # rook attacking bishop
                                              1,  # rook attacking rook
                                              1.4,  # rook attacking queen
                                             20),  # rook attacking king
                                            (0.1,  # queen attacking pawn
                                              0.3,  # queen attacking knight
                                              0.4,  # queen attacking bishop
                                              0.5,  # queen attacking rook
                                              1,  # queen attacking queen
                                             20),  # queen attacking king
                                            (0.2,  # king attacking pawn
                                              0.3,  # king attacking knight
                                              0.4,  # king attacking bishop
                                              0.7,  # king attacking rook
                                              0.5,  # king attacking queen
                                             0),)  # king attacking king is not possible
