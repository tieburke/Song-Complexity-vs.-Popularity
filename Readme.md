# Song Complexity vs. Popularity Analysis

## Overview

Data analysis project investigating the relationship between musical complexity and chart success using the McGill-Billboard Dataset. Demonstrates proficiency in data structures, statistical analysis, and Python optimization.

## Key Skills Demonstrated

- **Data Structures**: Implemented nested hash tables for efficient chord transition frequency analysis and multi-dimensional data storage
- **Algorithm Design**: O(N) operations with extensive optimization—reduced runtime by eliminating redundant computations across scoring functions
- **Statistical Analysis**: Linear regression modeling, distribution analysis, and z-score normalization for feature comparison
- **Python Mastery**: Dictionary manipulation, data processing pipelines, and performance optimization

## Technical Approach

**Complexity Scoring**: Analyzed five musical elements (tonic, meter, chord uniqueness, chord vocabulary, chord transitions) by measuring deviation from dataset norms. Complex songs feature rare or unusual musical structures.

**Popularity Scoring**: Combined chart performance metrics using the formula `(101 - peak_rank) × √(weeks_on_chart)` to create a normalized popularity index.

**Data Visualization**: Generated scatter plots, histograms, and regression analysis to reveal no significant correlation between complexity and popularity.

## Results

- **Performance**: ~0.3 second runtime processing entire dataset
- **Key Finding**: Musical complexity and commercial success are independent variables
- **Practical Value**: Challenges assumptions about complexity driving popularity—useful insight for music industry professionals

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Defining subjective "complexity" | Redefined as uniqueness relative to dataset norms rather than arbitrary values |
| Combining disparate frequency ranges | Developed normalization technique to integrate five independent scoring dimensions |
| Runtime inefficiency | Refactored to compute frequency tables once and reuse across all functions |

## Technologies

Python • Data Analysis • Statistical Modeling • Hash Tables • Algorithm Optimization
