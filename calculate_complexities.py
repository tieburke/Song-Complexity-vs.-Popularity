import create_songs
import get_song_data
import complexity_funcs

# BY making this file, I only create all these things once and then pass them to the functions that need them
# The first iteration of this, I had every function that needed something from create_songs or get_song_data create a new instance of it every time, and it took about 20 minutes

def calculate_complexities(songs):

    tonic_freq = get_song_data.get_tonic_freq(songs)
    tonic_stats = get_song_data.get_tonic_stats(songs, tonic_freq)

    metre_freq = get_song_data.get_metre_freq(songs)
    metre_stats = get_song_data.get_metre_stats(songs, metre_freq)

    num_chord_stats = get_song_data.get_num_chords_stats(songs)

    chord_freq = get_song_data.get_chord_freq(songs)
    chord_stats = get_song_data.get_chord_stats(songs, chord_freq)

    trans_freq = get_song_data.get_transition_freq(songs)
    trans_stats = get_song_data.get_transition_stats(songs, trans_freq)

    for song in songs.values():
        complexity_funcs.calc_complexity(song, songs, tonic_freq, tonic_stats, metre_freq, metre_stats, chord_freq, chord_stats, num_chord_stats, trans_freq, trans_stats)