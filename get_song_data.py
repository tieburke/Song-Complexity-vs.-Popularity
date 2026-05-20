"""
In this file, there are five measures of complexity that I gather data on.

High-level, I am defining more complex songs as more unique. Using the songs in my database, I am finding the frequency of four things:
a song's metre, a song's tonic, chords themselves, and chord transitions.

After finding the frequency of these things, given a song, I can find the proportion of other songs that are of the same type.

However, these values cannot be combined directly. For example, there are many more tonics that a song could be than metres, so the proportion
of other songs of the same metre will be higher than that of the same tonic. However, this is not fair to the complexity of a song because songs
typically have different tonics while it is more rare to have a unique metre than a unique tonic.

To account for this, for each of these four values, I will find the average proportion of other songs of the same type across all songs, and then
using this and the standard deviation of the same set, I will find a z-score for each value.

I can then add these four z-scores together and it will accurately represent the uniqueness and therefore complexity of a song.

The fifth element I am looking at is the number of unique chords in a song. I do not have to find the frequency of this, since it is just a numeric
value, so I will find the z-score of this directly and add it to the other four.
"""

import create_songs
import math


# frequency of different metres
def get_metre_freq(song_table):

    metre_table = {}
    num = 0

    for song in song_table.values():
        num += 1
        if song.metre in metre_table:
            metre_table[song.metre] += 1
        else:
            metre_table[song.metre] = 1
    
    for metre in metre_table.keys():
        metre_table[metre] = metre_table[metre] / num
    
    return metre_table

# average and standard deviation of the proportion of other songs with the same metre as a given song
def get_metre_stats(song_table, metre_freqs):
    
    # Get frequency for each song's metre
    metre_freq_list = [metre_freqs[song.metre] for song in song_table.values()]
    
    # Calculate mean and standard deviation
    mean = sum(metre_freq_list) / len(metre_freq_list)
    variance = sum((x - mean) ** 2 for x in metre_freq_list) / len(metre_freq_list)
    stdev = math.sqrt(variance)
    
    return (mean, stdev)



# frequencies of different tonics
def get_tonic_freq(song_table):

    tonic_table = {}
    num = 0

    for song in song_table.values():
        num += 1
        if song.tonic in tonic_table:
            tonic_table[song.tonic] += 1
        else:
            tonic_table[song.tonic] = 1
    
    for tonic in tonic_table.keys():
        tonic_table[tonic] = tonic_table[tonic] / num
    
    return tonic_table

# Average and standard deviation of tonic frequencies
def get_tonic_stats(song_table, tonic_freqs):
    
    # Get frequency for each song's tonic
    tonic_freq_list = [tonic_freqs[song.tonic] for song in song_table.values()]
    
    # Calculate mean and standard deviation
    mean = sum(tonic_freq_list) / len(tonic_freq_list)
    variance = sum((x - mean) ** 2 for x in tonic_freq_list) / len(tonic_freq_list)
    stdev = math.sqrt(variance)
    
    return (mean, stdev)



# frequency of individual chords
def get_chord_freq(song_table):

    chord_table = {}
    num = 0

    #iterate through each song
    for song in song_table.values():
        #iterate through each chord in that song
        num += len(song.chords)
        for chord, freq in song.chord_freq.items():
            if chord in chord_table:
                chord_table[chord] += freq
            else:
                chord_table[chord] = freq
    
    for chord in chord_table.keys():
        chord_table[chord] = chord_table[chord] / num

    return chord_table

# Computes the average and z-score for the sum of all chord frequencies in a song
def get_chord_stats(song_table, chord_freqs):
    
    # Get average chord frequency for each song
    chord_freq_list = []
    for song in song_table.values():
        avg_freq = sum(chord_freqs[chord] for chord in song.chords) / len(song.chords)
        chord_freq_list.append(avg_freq)
    
    # Calculate mean and standard deviation
    mean = sum(chord_freq_list) / len(chord_freq_list)
    variance = sum((x - mean) ** 2 for x in chord_freq_list) / len(chord_freq_list)
    stdev = math.sqrt(variance)
    
    return (mean, stdev)



# Computes the average and z-score for number of unique chords
def get_num_chords_stats(song_table):
    
    # Get number of unique chords for each song
    num_chords_list = [song.num_chords for song in song_table.values()]
    
    # Calculate mean and standard deviation
    mean = sum(num_chords_list) / len(num_chords_list)
    variance = sum((x - mean) ** 2 for x in num_chords_list) / len(num_chords_list)
    stdev = math.sqrt(variance)
    
    return (mean, stdev)



# I am analyzing the complexity of the chord progressions  by examining the frequency of a given transition
# These frequencies of a given transition will be used to calculate an average complexity of transition score
# Because I am seperately analyzing the complexity of given chord here, I will only look at the prefixes
# Going from a unique chord to a unique chord would too heavily weight this, so I am only looking at root notes
def get_transition_freq(song_table):

    # hash table of hash tables
    # each first chord has a hash table of next chords
    trans_freqs = {}

    num = 0

    for song in song_table.values():
        for chord, next_chord in zip(song.chords, song.chords[1:]):
            # if there is a hash table for this first chord
            num += 1
            if chord[0] in trans_freqs:
                # if this chord's hash table has the next chord yet
                if next_chord[0] in trans_freqs[chord[0]]:
                    trans_freqs[chord[0]][next_chord[0]] += 1
                else:
                    trans_freqs[chord[0]][next_chord[0]] = 1
            # if no hash table here yet, make it
            else:
                # make the hash table
                trans_freqs[chord[0]] = {}
                #add this first value
                trans_freqs[chord[0]][next_chord[0]] = 1
    
    for table in trans_freqs.values():
        for second in table.keys():
            table[second] /= num

    return trans_freqs

# Computes the average and z-score for transition frequencies
def get_transition_stats(song_table, trans_freqs):
    
    # Get average transition frequency for each song
    trans_freq_list = []
    for song in song_table.values():
        if len(song.chords) > 1:
            avg_trans = 0
            for chord, next_chord in zip(song.chords, song.chords[1:]):
                avg_trans += trans_freqs[chord[0]][next_chord[0]]
            avg_trans /= len(song.chords)
            trans_freq_list.append(avg_trans)
    
    # Calculate mean and standard deviation
    mean = sum(trans_freq_list) / len(trans_freq_list)
    variance = sum((x - mean) ** 2 for x in trans_freq_list) / len(trans_freq_list)
    stdev = math.sqrt(variance)
    
    return (mean, stdev)