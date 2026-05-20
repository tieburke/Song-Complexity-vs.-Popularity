# Song Complexity and Popularity Analyzer

## 1. Project Overview

This project analyzes and compares the complexity and popularity of songs. Using the McGill-Billboard Database, song complexity is determined by analyzing how unique different aspects of a song are relative to the rest of the database, and song popularity is determined based on given song chart performance data.

## 2. Relevant Data Structure Concepts

Dictionaries (hash tables) were most relevant to this project. After analysis, song objects were stored in a hash table keyed by index, and each song held several standard variables as well as a list of tuples. To calculate the frequencies of different song elements, additional hash tables were created with the element as the key and its frequency across all songs as the value.

The most complex application of this involved finding the frequency of chord transitions. To accomplish this, a hash table of hash tables was created: the outer key is the root note of the originating chord, and its value is an inner hash table where each key is the following chord and the value is the frequency of that transition across the entire database. This structure effectively represents a weighted directed graph, where nodes are chord root notes, edges represent transitions between them, and edge weights are the relative frequencies of those transitions in the dataset.

## 3. Project Workflow

**Inputs:** This project is designed to take its data from the McGill-Billboard Dataset. It requires songs in SALAMI (Structural Analysis of Large Amounts of Music Information) format to extract the musical information needed to calculate complexity, and it uses the dataset's chart performance metadata to calculate popularity. This method of determining complexity is most effective when working with a large collection of songs.

**Core Processing Logic:** The project calculates two scores for each song: complexity and popularity.

To determine complexity, five elements are analyzed: tonic, metre, number of unique chords, the chords themselves, and chord transitions. A frequency table is built for each of these elements across all songs. The mean and standard deviation of each frequency distribution are then computed, and each song is assigned a z-score measuring how far from average it sits in each of the five categories. These z-scores are then weighted and summed into a final complexity score. Tonic is weighted at 10% of the total, reflecting that tonal variety is common and expected across songs; the remaining four factors (metre, chord identity, number of unique chords, and chord transitions) are each weighted at 22.5%, as they are more signficant.

To determine popularity, two elements are analyzed: peak chart rank and weeks spent on the chart. These are combined with the formula `(101 - peak_rank) * sqrt(weeks_on_chart)`, which weights reaching a high rank heavily while still rewarding sustained chart presence.

**Outputs:** After scores are calculated, three graphs are produced:

- **Complexity vs. Popularity (Scatter Plot):** Each point represents one song, with its complexity score on the x-axis and popularity score on the y-axis. A linear regression line is overlaid along with its equation and R² value. The R² of 0.001 and a nearly flat slope indicate essentially no correlation between a song's complexity (as defined here) and its popularity — more musically unique songs are neither more nor less popular than conventional ones.

- **Complexity Distribution (Histogram):** Shows the distribution of complexity scores across all songs. The distribution is right-skewed, with the majority of songs clustering between 0.25 and 0.75, and a long tail of increasingly rare, highly complex songs extending to around 2.3. This indicates that most songs in the dataset share fairly conventional musical structures.

- **Popularity Distribution (Histogram):** Shows the distribution of popularity scores across all songs. The distribution is roughly bell-shaped and centered around 300–400, reflecting that most songs achieve moderate chart performance, with fewer songs at the extremes of very low or very high popularity.

## 4. Performance

Most operations are O(N), where N is the number of songs. However, the dominant operations are those that iterate over every chord in every song all of these are O(C), where C is the number of chords. Therefore, the overall complexity is O(C).

The runtime to calculate everything is roughly **0.3 seconds**.

## 5. Challenges

Broadly, the biggest challenge was determining how to accurately measure and score song complexity. Assigning arbitrary numeric values to musical elements was inaccurate and required extensive music theory research.

I solved this by defining complexity as uniqueness relative to the dataset. For each musical element (metre, tonic, chord, chord transition). A song with a rare time signature or unusual chord progressions is more complex because it is rarer.

The second challenge was combining these frequency values into a single score. The frequencies could not be added directly, because different elements have very different natural frequency ranges (e.g., there are far fewer possible metres than possible chord combinations, so metre frequencies are naturally higher). To normalize across these differences, z-scores were computed for each element, allowing them to be added together.

A third challenge was runtime. The first iteration of the code recomputed frequency tables inside every function that needed them, causing each of the five scoring functions to independently iterate over the entire dataset. This made a full run take roughly 20 minutes. The fix was to compute all frequency tables and statistics once in and pass them as arguments into each function.

## 6. Improvements

The current chord transition analysis computes the average frequency of each chord pair in a song, then takes the z-score of that average. While this captures something about how conventional a song's progressions are, it does not measure how closely a song follows expected harmonic patterns for its tonic. In practice, most Western music uses well-established chord patters and songs often make themseleves more complex by deviating from these patterns.

A more accurate complexity measure would compare each song's transitions against expected progressions for its key, but this would require extensive music theory research. I ended up not doing this because it does not involve especially interesting data structure implementation and would require significant music theory research.

## 7. Learning

Working on this project significantly improved my familiarity with Python's built-in data structures, especially dictionaries. The nested dictionary structure used for chord transition frequencies also provided hands-on experience implementing bigram tables, a technique central to natural language processing.

## 8. Real-World Relevance

This project demonstrates that there is no meaningful correlation between musical complexity (as measured by uniqueness of structure) and popularity. This finding could be useful to songwriters and producers, providing evidence that making a song more musically complex does not reliably improve or hurt its chart performance.

## 9. Use of AI Tools

AI was used most significantly in the initial brainstorming phase. Starting from broad topic ideas, AI helped me refine the concept and think through what implementation might look like. I also consulted AI for music theory questions. During coding, I used AI occasionally used to help translate pseudocode into Python when stuck on syntax or standard library usage.
