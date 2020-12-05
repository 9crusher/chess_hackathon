import chess


class StubAgent:
    """
    Your agent class. Please rename this to {TeamName}Agent, and this file to {TeamName}.py
    """
    depth = 3

    cache = {}

    opening = {}

    def __init__(self, is_white):
        """
        Constructor, initialize your fields here.
        :param is_white: Initializes the color of the agent.
        """
        self.is_white = is_white

    @staticmethod
    def get_team_name():
        """
        Report your team name. Used for scoring purposes.+
        """
        return "Blatantly Extraneous"

    def heuristic(self, board):
        """
        Determine whose favor the board is in, and by how much.
        Positive values favor white, negative values favor black.

        Modify this. It sucks. Consider incorporating board state.
        At present, this just sums the scores of all the pieces.

        :param board:
        :return: Returns the estimated utility of the board state.
        """
        # Evaluate scores of each piece
        
        value = sum(
            get_piece_utility(board.piece_at(square))
            #attackers(board.piece_at(square))
            if board.piece_at(square) is not None else 0
            for square in chess.SQUARES
        )

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
        
        if (board in opening){

        }else {
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
        }

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
