import chess.pgn

with open('src/ficsgamesdb_2019_standard2000_nomovetimes_172500.pgn') as f:
    lines = list(f.read().splitlines())
    lines = list(filter(lambda e: e != ' ', lines))
    lines =  list(map(lambda x: x.split(), lines))
    print(lines[0:20])