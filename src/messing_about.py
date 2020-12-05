import chess.pgn

pgn = open("./ficsgamesdb_2019_standard2000_nomovetimes_172500.pgn")

games = []
while pgn:
    chess.pgn.read_game(pgn)