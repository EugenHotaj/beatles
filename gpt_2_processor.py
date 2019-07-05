"""Dataset processor for GPT-2.

Reformats The Beatles' lyrics dataset and writes it out to a file. For each 
song, the title is written on the first line, the writers on the second, then
the lyrics on the next N lines. Finally, two blank lines are written before
the start of the next song. E.g.:
<Song 1 Title>
<Song 1 Writer(s)>
<Song 1 Lyrics>
<Song 1 Lyrics>
...
<Song 1 Lyrics>


<Song 2 Title>
<Song 2 Writer(s)>
<Song 2 Lyrics>
<Song 2 Lyrics>
...
<Song 1 Lyrics>


...
...
...


<Song m Title>
<Song m Writer(s)>
<Song m Lyrics>
<Song m Lyrics>
<Song m Lyrics>
"""

if __name__ == '__main__':
    with open('dataset.txt', 'r') as file_:
        songs = file_.readlines()

    dataset = ''
    for song in songs:
        song = song.strip()
        title, author, song = song.split('\t')
        dataset += "{}\n{}\n".format(title, author)
        lyrics = song.split('\\')
        for lyric in lyrics:
            dataset += lyric + '\n'
        dataset += '\n\n'

    with open('gpt_2_dataset.txt', 'w') as file_:
        file_.write(dataset)


        
