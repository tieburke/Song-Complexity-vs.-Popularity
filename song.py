class Song:
    def __init__(self, index, title, artist, peak_rank, weeks_on_chart, metre, tonic, chords, num_chords=None, chord_freq=None, complexity_score=None, popularity_score=None):
        self.index = index
        self.title = title
        self.artist = artist
        
        self.peak_rank = peak_rank
        self.weeks_on_chart = weeks_on_chart

        self.metre = metre
        self.tonic = tonic
        self.chords = chords # list of every chord in the song

        self.num_chords = num_chords # number of unique chords
        self.chord_freq = chord_freq if chord_freq is not None else {} #frequency of each chord in the song

        self.complexity_score = complexity_score
        self.popularity_score = popularity_score

    def set_chord_data(self, num_chords, chord_freq):
        self.num_chords = num_chords
        self.chord_freq = chord_freq
    
    def set_complexity_score(self, complexity_score):
        self.complexity_score = complexity_score

    def set_popularity_score(self, popularity_score):
        self.popularity_score = popularity_score