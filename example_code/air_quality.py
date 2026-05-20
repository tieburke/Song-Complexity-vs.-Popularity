#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional


def load_air_quality(path_or_url: str) -> pd.DataFrame:
	"""Load air quality data from a local path or a URL into a DataFrame."""
	# Parse the first column as datetime and set it as the index so callers``
	# can rely on a datetime index and station columns only.
	# Use index_col=0 to avoid keeping the datetime as a regular column.
	df = pd.read_csv(path_or_url, parse_dates=[0], index_col=0)
	return df


def compute_station_average(df: pd.DataFrame, station: str) -> float:
	"""Return the mean of the given station column, ignoring non-numeric values and NaNs.

	We call `pd.to_numeric(..., errors='coerce')` to defensively convert the column
	to numeric values. Non-convertible entries (for example, unexpected text)
	are converted to `NaN` so that downstream aggregations like `.mean()` will
	ignore them. This keeps the function robust to minor data issues in the CSV.
	"""
	s = pd.to_numeric(df.get(station), errors="coerce")
	return s.mean()


def compute_overall_mean(df: pd.DataFrame, columns: Optional[list] = None) -> float:
	"""Compute the mean across the provided columns, or across all data
	columns (all station columns) when `columns` is None. `load_air_quality`
	sets the datetime index so all remaining columns are treated as station data.
	"""
	if columns:
		return df[columns].stack().mean()
	# compute mean across all columns (all stations)
	return df.stack().mean()


def compute_station_median(df: pd.DataFrame, station: str) -> float:
	"""Return the median of a named station column (coerce non-numeric to NaN)."""
	s = pd.to_numeric(df.get(station), errors="coerce")
	return s.median()


def plot_air_quality(df: pd.DataFrame) -> plt.Axes:
	"""Create a new figure, plot the DataFrame on it, and return the Axes.
	"""
	fig, ax = plt.subplots()
	# `load_air_quality` sets a datetime index; plot station columns vs index.
	df.plot(ax=ax)
	ax.set_title("Air quality NO2 (all stations)")
	ax.set_xlabel("datetime")
	return ax

def main():
	# Simple demo: read from the upstream URL and show a plot interactively.
	url = "https://raw.githubusercontent.com/pandas-dev/pandas/refs/heads/main/doc/data/air_quality_no2.csv"
	df = load_air_quality(url)
	print(df.head())

	# Choose a sample station (second column) for per-station examples
	if df.shape[1] > 0:
		# after load_air_quality the columns are station names (index is datetime)
		station_name = df.columns[0]
		avg = compute_station_average(df, station_name)
		median = compute_station_median(df, station_name)
		print(f"{station_name} average: {avg:.6f}")
		print(f"{station_name} median: {median:.6f}")

	# Compute overall mean across all station columns (ignores first datetime column)
	overall = compute_overall_mean(df)
	print(f"overall mean (all stations): {overall:.6f}")

	# Plot and display
	plot_air_quality(df)
	plt.show()

if __name__ == "__main__":
    main()