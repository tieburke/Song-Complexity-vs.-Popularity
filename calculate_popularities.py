import math
import create_songs

# multiplies the peak rank by the square root of the number of weeks in the top 100
# this accounts for both while keeping the importance of hitting a high rank intact

def calculate_popularities(songs):

    for song in songs.values():
        # Calculate the raw score
        intensity = 101 - song.peak_rank
        longevity = math.sqrt(song.weeks_on_chart)
    
        song.set_popularity_score(intensity * longevity)
