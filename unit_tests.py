#!/usr/bin/env python3

import unittest
from unittest.mock import patch, mock_open
import create_songs
import get_song_data
import calculate_popularities
import complexity_funcs
import song

"""
To test my functions, I created two "songs" in the folder "test_songs" that are in the same format as this database

I put together the first song, and had AI create the second one. None of them could reasonably be played etc. but they fit the same format as a song.

To test a given value, I calculated/found it by hand and then compared it to the return from the functions.
"""

class unitTests(unittest.TestCase):
   
    test_song_1_chords = [('D','maj'), ('E','min'), ('C','maj')]

    test_song_2_chords = [
        # Intro
        ("C", "maj"), ("F", "maj"), ("G", "maj"), ("C", "maj"),
        # Verse 1
        ("C", "maj"), ("Am", "min"), ("F", "maj"), ("G", "maj"),
        ("C", "maj"), ("Am", "min"), ("F", "maj"), ("G", "maj"),
        # Chorus 1
        ("F", "maj"), ("G", "maj"), ("Em", "min"), ("Am", "min"),
        ("F", "maj"), ("G", "maj"), ("C", "maj"), ("C", "maj"),
        # Verse 2
        ("C", "maj"), ("Am", "min"), ("F", "maj"), ("G", "maj"),
        ("C", "maj"), ("Am", "min"), ("F", "maj"), ("G", "maj"),
        # Bridge
        ("D", "min"), ("G", "maj"), ("D", "min"), ("G", "maj"),
        # Chorus 2
        ("F", "maj"), ("G", "maj"), ("Em", "min"), ("Am", "min"),
        ("F", "maj"), ("G", "maj"), ("C", "maj"), ("C", "maj"),
        # Outro
        ("F", "maj"), ("C", "maj")
    ]


    ### Creates songs dict from the test songs ###
    def get_dummy_songs(self):
        #First "song" I put together
        song1 = song.Song(
            index=1, title="Test Song", artist="Tiernan Burke", 
            peak_rank=10, weeks_on_chart=25, metre="6/8", tonic="G", 
            chords=self.test_song_1_chords, num_chords=3
        )
        
        #longer song I had AI write (FYI, still not a song)
        song2 = song.Song(
            index=2, title="longer song", artist="Gemini", 
            peak_rank=52, weeks_on_chart=16, metre="4/4", tonic="C", 
            chords=self.test_song_2_chords, num_chords=6
        )
        
        return {1: song1, 2: song2}


    def test_extract_info(self):
        # test getting a bad file path
        results = create_songs.extract_info("not_a_file")
        self.assertEqual(results, None)

        results = create_songs.extract_info("test_songs/test_song_1.txt")
        self.assertEqual(results[0], "6/8")
        self.assertEqual(results[1], "G")
        self.assertEqual(results[2], self.test_song_1_chords)


        results = create_songs.extract_info("test_songs/test_song_2.txt")
        self.assertEqual(results[0], '4/4')
        self.assertEqual(results[1], 'C')
        self.assertEqual(results[2], self.test_song_2_chords)

    
    def test_parse_chords(self):
        raw_chords = ["C:maj", "Am:min", "F:maj", "G:maj"]
        expected_parsed = [("C", "maj"), ("Am", "min"), ("F", "maj"), ("G", "maj")]

        results = create_songs.parse_chords(raw_chords)
        
        self.assertEqual(results, expected_parsed)


    def test_calculate_popularities(self):
        songs = self.get_dummy_songs()
        calculate_popularities.calculate_popularities(songs)

        # Song 1 Expected: 
        # intensity = 101 - 10 = 91 
        # longevity = sqrt(25) = 5 
        # score = 91 * 5 = 455
        self.assertAlmostEqual(songs[1].popularity_score, 455.0)

        # Song 2 Expected: 
        # intensity = 101 - 52 = 49
        # longevity = sqrt(16) = 4 
        # score = 49 * 4 = 196
        self.assertAlmostEqual(songs[2].popularity_score, 196.0)


    def test_num_chords_complexity(self):
        songs = self.get_dummy_songs()
        
        # Give a mock mean of 4.0 and standard deviation of 2.0
        mock_stats = (4.0, 2.0) 

        # Song 1 has 3 unique chords.
        # z_score = abs(3 - 4.0) / 2.0 = 0.5 
        # expected final = 0.5 * 0.225 = 0.1125 
        result_1 = complexity_funcs.num_chords_complexity(songs[1], mock_stats)
        self.assertAlmostEqual(result_1, 0.1125)

        # Song 2 has 6 unique chords.
        # z_score = abs(6 - 4.0) / 2.0 = 1.0 
        # expected final = 1.0 * 0.225 = 0.225 
        result_2 = complexity_funcs.num_chords_complexity(songs[2], mock_stats)
        self.assertAlmostEqual(result_2, 0.225)


    def test_get_metre_freq(self):
        songs = self.get_dummy_songs()
        
        # We have two songs total: One is "6/8", one is "4/4"
        freqs = get_song_data.get_metre_freq(songs)

        # The frequency of boht should just be 0.5
        self.assertEqual(len(freqs), 2)
        self.assertAlmostEqual(freqs["6/8"], 0.5)
        self.assertAlmostEqual(freqs["4/4"], 0.5)
        
    def test_get_tonic_freq(self):
        songs = self.get_dummy_songs()
        
        # We have two songs total: One is "G", one is "C" 
        freqs = get_song_data.get_tonic_freq(songs)

        # The frequency of both should just be 0.5
        self.assertEqual(len(freqs), 2)
        self.assertAlmostEqual(freqs["G"], 0.5)
        self.assertAlmostEqual(freqs["C"], 0.5)
    
    def test_get_chord_freq(self):
        # Create another song with chord_freq data populated
        song_test = song.Song(
            index=3, title="Chord Freq Test", artist="", 
            peak_rank=0, weeks_on_chart=0, metre="", tonic="", 
            chords=[('C', 'maj'), ('F', 'maj'), ('C', 'maj')], 
            num_chords=2,
            chord_freq={('C', 'maj'): 2, ('F', 'maj'): 1} # Explicitly pass the frequencies
        )
        songs = {1: song_test}
        
        freqs = get_song_data.get_chord_freq(songs)
        
        # Only going to find the chord frequencies from this one song instead of all of them
        # Total chords = 3. 
        # ('C', 'maj') appears twice (2/3), ('F', 'maj') appears once (1/3)
        self.assertAlmostEqual(freqs[('C', 'maj')], 2.0 / 3.0)
        self.assertAlmostEqual(freqs[('F', 'maj')], 1.0 / 3.0)

    def test_get_transition_freq(self):
        # Create another song to transition counting
        song_test = song.Song(
            index=4, title="Transition Test", artist="", 
            peak_rank=0, weeks_on_chart=0, metre="", tonic="", 
            chords=[('C', 'maj'), ('F', 'maj'), ('G', 'maj'), ('C', 'maj')], 
            num_chords=3
        )
        songs = {1: song_test}
        
        trans_freqs = get_song_data.get_transition_freq(songs)
        
        # This only looks at the prefixes
        # Transitions: C -> F, F -> G, G -> C (Total = 3 transitions)
        self.assertAlmostEqual(trans_freqs['C']['F'], 1.0 / 3.0)
        self.assertAlmostEqual(trans_freqs['F']['G'], 1.0 / 3.0)
        self.assertAlmostEqual(trans_freqs['G']['C'], 1.0 / 3.0)
        
        # Verify that it properly isolated the roots and didn't use the full tuples
        self.assertNotIn(('C', 'maj'), trans_freqs)

if __name__ == '__main__':
    unittest.main()