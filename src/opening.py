import chess

class Opening:
    _openings = {}

    def __init__(self):
        self._import_openings()

    def _import_openings(self):
        print(chess.STARTING_BOARD_FEN)
        self._openings = {
            chess.STARTING_BOARD_FEN:"e2e4" #Berlin Defense
        }

    def get_openings(self):
        return self._openings