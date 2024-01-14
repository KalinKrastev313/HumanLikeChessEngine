HumanLikeChessEngine

Currently the chess engine has no API, but you can make it play against itself by running main.py
There would be created a game_pgn.txt with the notation of the resulting game.
To review the game, I suggest you use publicly available tool like https://lichess.org/analysis
Just paste the text in the PGN text box below the board and click import PGN.

Currently, the engine is set to work at a depth of 4 halfmoves.
The engine uses min max algorithm with alpha-beta pruning.
You can tweak it's evaluation function by just changing the values in positional_values_dict and piece_values_dict .

Additional positional values to be considered as well as performance improvements are currently in production.
