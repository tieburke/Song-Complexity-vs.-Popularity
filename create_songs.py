import os
import pandas as pd
from song import Song

def extract_csv():
    # TODO: take this from user input
    
    index_df = pd.read_csv('billboard-2.0-index.csv')
    #makes the songs accessible by index
    index_df = index_df.set_index('id')
    index_df.index = index_df.index.astype(str).str.zfill(4)

    return index_df


def extract_info(filePath):
    chords = []
    flag = 0
    
    if os.path.exists(filePath):
        # using with to have python automatically close it
        with open(filePath, 'r') as f:
            for line in f:

                line_elements = line.split()

                #going through each element and checking if it is a valid chord
                for i in line_elements:

                    # checking for metre or tonic
                    if(i == 'metre:'):
                        flag = 1
                    elif(flag == 1):
                        metre = i
                        flag = 0

                    if (i == 'tonic:'):
                        flag = 2
                    elif(flag == 2):
                        tonic = i
                        flag = 0

                    # making sure the second character is a colon
                    if (':' in i):
                        if i[1] == ':' or i[2] == ':':
                            chords.append(i)
        
        chords = parse_chords(chords)
        return (metre, tonic, chords)
    
    #return null if the filePath doesn't exist
    else:
        return None


# helper function to split chords
def parse_chords(chords):
    parsed_chords = []
    for chord in chords:
        prefix, suffix = chord.split(':')
        parsed_chords.append((prefix, suffix))
    return parsed_chords


def songs():
    index_df = extract_csv()

    # creating a hash table of what will be song objects
    song_table = {}

    #elements of the file path:
    cwd = os.getcwd()
    mcGill = "McGill-Billboard"
    file_name = "salami_chords.txt"
    indeces = [f"{i:04d}" for i in range(0, 1301)]

    for index in indeces:
        full_path = os.path.join(cwd, mcGill, index, file_name)
        results = extract_info(full_path)

        if results is None:
            continue

        #getting other info from the csv
        title = index_df.loc[index, 'title']
        artist = index_df.loc[index, 'artist']

        peak_rank = index_df.loc[index, 'peak_rank']
        weeks_on_chart = index_df.loc[index, 'weeks_on_chart']

        new_song = Song(index, title, artist, peak_rank, weeks_on_chart, results[0], results[1], results[2])
        song_table[index] = new_song
    
    calculate_chords(song_table)
    return song_table


def calculate_chords(song_table):
    for song in song_table.values():
        chord_freq = {}
        for chord in song.chords:
            if chord in chord_freq:
                chord_freq[chord] += 1
            else:
                chord_freq[chord] = 1
        song.set_chord_data(len(chord_freq), chord_freq)