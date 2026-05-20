#!/usr/bin/env python3

import unittest
import pandas as pd

from air_quality import (
    load_air_quality,
    compute_station_average,
    compute_overall_mean,
    compute_station_median,
)


class TestAirQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_path = str("air_quality_sample.csv")

    def test_load(self):
        df = load_air_quality(self.sample_path)
        self.assertIn("station_a", df.columns)
        self.assertIn("station_b", df.columns)
        self.assertEqual(len(df), 4)

    def test_compute_station_average(self):
        df = load_air_quality(self.sample_path)
        expected = (10.0 + 12.0 + 11.5) / 3.0
        actual = compute_station_average(df, "station_a")
        self.assertAlmostEqual(expected, actual, places=6)

    def test_compute_overall_mean(self):
        df = load_air_quality(self.sample_path)
        # numeric values: 10.0,12.0,11.5,12.0,11.0,13.0,14.0 (note one missing in station_a)
        numeric_values = [10.0, 12.0, 11.5, 12.0, 11.0, 13.0, 14.0]
        expected = sum(numeric_values) / len(numeric_values)
        actual = compute_overall_mean(df)
        self.assertAlmostEqual(expected, actual, places=6)

    def test_compute_station_median(self):
        df = load_air_quality(self.sample_path)
        # station_a non-missing values: [10.0,12.0,11.5] -> median 11.5
        expected = 11.5
        actual = compute_station_median(df, "station_a")
        self.assertAlmostEqual(expected, actual, places=6)


if __name__ == "__main__":
    unittest.main()
