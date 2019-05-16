"""Probabilistic bigram language model."""

import collections

import numpy as np

START_SONG = 'XXSS'  # Token for the start of a new song.
START_LINE = 'XXSL'  # Token for the start of a new line.
END_LINE = 'XXEL'  # Token for the end of a line.
END_SONG = 'XXES'  # Token for the end of a song.

PREFIXES = ('(')
# NOTE: Check `...` before `.`.
SUFFIXES = (')', '?', '!', ',' , '...', '.', ':', '"')

class ProbabilisticBigramLanguageModel(object):
    """A probabilistic bigram language model.

    Given a list of bigrams, the model builds a probability distribution
    over the bigrams.

    TODO(eugenhotaj): Flesh out.
    """

    def __init__(self):
        self._model = collections.defaultdict(collections.Counter)

    def fit(self, bigrams):
        for curr_word, next_word in bigrams:
            self._model[curr_word].update({next_word: 1})

    def predict(self, curr_word):
        words, counts = list(zip(*self._model[curr_word].most_common()))
        counts = np.array(counts)
        probs = counts / np.sum(counts)
        return np.random.choice(words, p=probs)


def process_token(token):
    """Splits out prefixes and suffixes from the token."""
    # Split prefixes.
    prefixes = []
    is_clean = False
    while not is_clean:
        is_clean = True
        for prefix in PREFIXES:
            if token.startswith(prefix):
                is_clean = False
                prefixes.append(token[:len(prefix)])
                token = token[len(prefix):]

    # Split suffixes.
    suffixes = []
    is_clean = False
    for suffix in SUFFIXES:
        is_clean = True
        if token.endswith(suffix):
            is_clean = False
            suffixes.append(token[-len(suffix):])
            token = token[:-len(suffix)]
    return prefixes + [token] + suffixes


def create_bigrams(line):
    """Returns bigrams of the line with token prefixes and suffixes expanded."""
    line_tokens = line.split(' ')
    tokens = []
    for token in line_tokens:
        tokens.extend(process_token(token))
    bigrams = []
    for i in range(len(tokens) - 1):
        curr_word, next_word = tokens[i], tokens[i + 1]
        bigrams.append((curr_word, next_word))
    return bigrams

if __name__ == '__main__':
    with open('songs.txt') as file_:
        songs = file_.readlines()
    lines = []
    for song in songs:
        song = song.strip()
        title, author, lyrics = song.split('\t')
        lyrics = '{} {} {}'.format(START_SONG, lyrics, END_SONG)
        lines.extend(lyrics.split('\\'))

    bigrams = []
    for line in lines:
        # TODO(eugenhotaj): There is probably a smarter way to handle this.
        if not line.endswith(END_SONG):
            line = '{} {} {} {}'.format(START_LINE, line, END_LINE, START_LINE)
        bigrams.extend(create_bigrams(line))

    model = ProbabilisticBigramLanguageModel()
    model.fit(bigrams)

    song = []
    pred = START_SONG
    while not pred == END_SONG:
        pred = model.predict(pred)
        if pred == END_LINE:
            song.append("\n")
        elif pred in (START_SONG, START_LINE, END_SONG):
            pass
        elif pred in PREFIXES:
            song.append(pred)
        elif pred in SUFFIXES:
            song[-1] = song[-1][:-1] + pred + " "
        else:
            song.append(pred + " ")
    print("".join(song))
