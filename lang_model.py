"""Probabilistic bigram language model."""

START_SONG = "XXSS"
NEW_LINE = "XXNL"
END_SONG = "XXES"

if __name__ == '__main__':
    with open('songs.txt') as file_:
        lines = file_.readlines()
    lyrics = []
    for line in lines:
        line = line.strip()
        title, author, line = line.split('\t')
        lyrics.extend(line.split('\\'))
    print(len(lyrics))
