import calculate_complexities
import calculate_popularities
import create_songs
import numpy as np

import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

"""
if __name__ == "__main__":
    import time

start_time = time.perf_counter() # Start the timer
"""

songs = create_songs.songs()

calculate_complexities.calculate_complexities(songs)
calculate_popularities.calculate_popularities(songs)

pops = np.array([song.popularity_score for song in songs.values()])
comps = np.array([song.complexity_score for song in songs.values()])

"""
end_time = time.perf_counter()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
"""

plt.scatter(x=comps, y=pops, color='blue', label='Data Points')
plt.xlabel('Complexity Score')
plt.ylabel('Popularity Score')
plt.title('Complexity vs. Popularity')

m, b = np.polyfit(comps, pops, 1)

pops_pred = m * comps + b
r_squared = r2_score(pops, pops_pred)

plt.plot(comps, m*comps + b, color='red', label=f'Fit: y={m:.2f}x+{b:.2f}, $R^2 = {r_squared:.3f}$')

plt.legend()
plt.show()

plt.xlabel('Complexity Score')
plt.ylabel('Frequency')
plt.title('Complexity Distribution')
plt.hist(comps)
plt.show()

plt.xlabel('Popularity Score')
plt.ylabel('Frequency')
plt.title('Popularity Distribution')
plt.hist(pops)
plt.show()