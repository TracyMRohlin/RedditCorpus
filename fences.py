#!/usr/bin/env python
__author__ = 'tracyrohlin'

import argparse
import numpy as np

from Karma_Graph import load_data

def fences(filepath):
    data = load_data(filepath)
    lower = np.percentile(data, 25)
    upper = np.percentile(data, 75)
    interquartile_range = upper - lower
    lower_fence = lower - 1.5 * interquartile_range
    upper_fence = upper + 1.5 * interquartile_range
    return lower_fence, upper_fence

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Computes the lower and upper fence from the data found in Karma Scores.csv")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    args = parser.parse_args()
    print fences(args.filepath)