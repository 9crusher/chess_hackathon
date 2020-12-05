import chess
brd = chess.Board()

# pattern follows: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
for move in brd.legal_moves:
    #print(move)
    pass

print(chess.Move.from_uci("e2e4"))
#print(chess.Move(chess.Square("e2"), chess.Square("e4")))
