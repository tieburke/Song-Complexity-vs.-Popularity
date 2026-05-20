import create_songs
import get_song_data
import math
import song


# overall complexity score function
def calc_complexity(song, song_table, tonic_freqs, tonic_stats, metre_freqs, metre_stats, chord_freqs, chord_stats, num_chords_stats, trans_freq, trans_stats):
    complexity = (
        tonic_complexity(song, song_table, tonic_freqs, tonic_stats)
        + metre_complexity(song, song_table, metre_freqs, metre_stats)
        + chord_complexity(song, song_table, chord_freqs, chord_stats)
        + num_chords_complexity(song, num_chords_stats)
        + progression_complexity(song, trans_freq, trans_stats)
    )

    song.set_complexity_score(complexity)

# how common the key is
# weighted as 10% of total complexity
def tonic_complexity(song, song_table, tonic_freqs, stats):
    
    complexity = tonic_freqs[song.tonic]
    
    z_score = abs(complexity - stats[0])/stats[1]

    return z_score * 0.1

    

#how commone the metre is
# weighted as 22.5% of the total complexity
def metre_complexity(song, song_table, metre_freqs, stats):

    complexity = metre_freqs[song.metre]

    z_score = abs(complexity - stats[0])/stats[1]

    return z_score * 0.225



# average uniquness of the chords
# weighted as 22.5% of the total complexity
def chord_complexity(song, song_table, chord_freqs, stats):
    
    #finding the average complexity of all the chords in the song
    complexity = 0
    for chord in song.chords:
        complexity += chord_freqs[chord]
    complexity /= len(song.chords)
    
    z_score = abs(complexity - stats[0])/stats[1]
    
    return z_score * 0.225


# uniquness of the number of chords relative to the average
# weighted as 22.5% of the total complexity
def num_chords_complexity(song, stats):
    
    z_score = abs(song.num_chords - stats[0]) / stats[1]
    
    return z_score * 0.225



# average uniquness of chord transitions
# weighted as 22.5% of total complexity
def progression_complexity(song, trans_freqs, stats):

    avg_trans = 0
    for chord, next_chord in zip(song.chords, song.chords[1:]):
        avg_trans += trans_freqs[chord[0]][next_chord[0]]
    
    avg_trans /= len(song.chords)

    z_score = abs(avg_trans - stats[0])/stats[1]

    return z_score * 0.225



### TESTS ###
"""
song_table = create_songs.songs()

for song in song_table.values():
    print(tonic_complexity(song))
    print(metre_complexity(song))
    print(chord_complexity(song))
    print(num_chords_complexity(song))
    print(progression_complexity(song))
    print()
"""