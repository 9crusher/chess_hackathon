import chess

class StubAgent:
    """
    Your agent class. Please rename this to {TeamName}Agent, and this file to {TeamName}.py
    """
    depth = 3

    cache = {}

    opens = {}

    def __init__(self, is_white):
        """
        Constructor, initialize your fields here.
        :param is_white: Initializes the color of the agent.
        """
        self.is_white = is_white
        self.opens = openings()

    @staticmethod
    def get_team_name():
        """
        Report your team name. Used for scoring purposes.+
        """
        return "blatantly extraneous"

    def check_value(self, board):
        if board.is_check():
            if board.turn == chess.WHITE and self.is_white or (board.turn == chess.BLACK and not self.is_white):
                return -20
            else:
                return 20
        return 0

    def legal_moves(self, board):
        original = board.turn
        board.turn = chess.WHITE
        white_moves = len(list(board.legal_moves))
        board.turn = chess.BLACK
        black_moves = len(list(board.legal_moves))
        board.turn = original
        return white_moves - black_moves if self.is_white else black_moves - white_moves

    def heuristic(self, board):
        """
        Determine whose favor the board is in, and by how much.
        Positive values favor white, negative values favor black.
        Modify this. It sucks. Consider incorporating board state.
        At present, this just sums the scores of all the pieces.
        :param board:
        :return: Returns the estimated utility of the board state.
        """
        value = sum(
            get_piece_utility(board.piece_at(square))
            #attackers(board.piece_at(square))
            if board.piece_at(square) is not None else 0
            for square in chess.SQUARES
        )

        value += self.check_value(board)
        lm = self.legal_moves(board)
        #print(lm)
        value += lm


        # If this is a draw, value is 0 (same for both players)
        if board.can_claim_draw():
            value = 0

        return value

    def make_move(self, board):
        """
        Determine the next move to make, given the current board.
        :param board: The chess board
        :return: The selected move
        """
        global_score = -1e8 if self.is_white else 1e8
        chosen_move = None

        if str(board) in self.opens:
            chosen_move = self.opens[str(board)]
        else:
            for move in board.legal_moves:
                board.push(move)

                local_score = self.minimax(board, self.depth - 1, not self.is_white, -1e8, 1e8)
                self.cache[hash_board(board, self.depth - 1, not self.is_white)] = local_score

                if self.is_white and local_score > global_score:
                    global_score = local_score
                    chosen_move = move
                elif not self.is_white and local_score < global_score:
                    global_score = local_score
                    chosen_move = move

                board.pop()

        return chosen_move

    def minimax(self, board, depth, is_maxing_white, alpha, beta):
        """
        Minimax implementation with alpha-beta pruning.
        Source: https://github.com/devinalvaro/yachess
        :param board: Chess board
        :param depth: Remaining search depth
        :param is_maxing_white: Whose score are we maxing?
        :param alpha: Alpha-beta pruning value
        :param beta: Alpha-beta pruning value
        :return: The utility of the board state
        """
        # Check if board state is in cache
        if hash_board(board, depth, is_maxing_white) in self.cache:
            return self.cache[hash_board(board, depth, is_maxing_white)]

        # Check if game is over or we have reached maximum search depth.
        if depth == 0 or not board.legal_moves:
            self.cache[hash_board(board, depth, is_maxing_white)] = self.heuristic(board)
            return self.cache[hash_board(board, depth, is_maxing_white)]

        # General case
        best_score = -1e8 if is_maxing_white else 1e8
        for move in board.legal_moves:
            board.push(move)

            local_score = self.minimax(board, depth - 1, not is_maxing_white, alpha, beta)
            self.cache[hash_board(board, depth - 1, not is_maxing_white)] = local_score

            if is_maxing_white:
                best_score = max(best_score, local_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, local_score)
                beta = min(beta, best_score)

            board.pop()

            if beta <= alpha:
                break
        self.cache[hash_board(board, depth, is_maxing_white)] = best_score
        return self.cache[hash_board(board, depth, is_maxing_white)]


def hash_board(board, depth, is_maxing_white):
    """
    Get a representation of the system that we can cache.
    """
    return str(board) + ' ' + str(depth) + ' ' + str(is_maxing_white)


def get_piece_utility(piece):
    """
    Get the utility of a piece.
    :return: Returns the standard chess score for the piece, positive if white, negative if black.
    """
    piece_symbol = piece.symbol()
    is_white = not piece_symbol.islower()

    lower = piece_symbol.lower()

    score = 1 if is_white else -1

    if lower == 'p':
        score *= 1
    elif lower == 'n':
        score *= 3
    elif lower == 'b':
        score *= 3
    elif lower == 'r':
        score *= 5
    elif lower == 'q':
        score *= 9
    elif lower == 'k':
        score *= 1_000_000
    return score

def openings():
    return {
        str(chess.STARTING_FEN):"e2e4", #Berlin Defense
        str(chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")):"e7e5",
        str(chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")):"g1f3",
        str(chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")):"b8c6"
    }