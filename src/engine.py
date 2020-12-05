# This is the provided runner for local execution. You don't really need to modify it.
# It will save images of the game for you in the images folder.

import chess
import chess.engine
import chess.svg

from stub import StubAgent


def play():
    board = chess.Board()

    white = StubAgent(True)
    black = StubAgent(False)

    count = 0

    while not board.is_game_over():
        if count % 2 == 0:
            chosen_move = white.make_move(board.copy())
        else:
            chosen_move = black.make_move(board.copy())
        board.push(chosen_move)
        s = chess.svg.board(board)
        move_file = open("images/move{}.svg".format(count), "w")
        move_file.truncate()
        move_file.write(s)
        move_file.close()
        count += 1


play()
