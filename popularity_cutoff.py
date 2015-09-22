#!/usr/bin/env python

__author__ = 'tracyrohlin'

import argparse
import numpy as np

from Karma_Graph import load_data

def compute_cutoff(filepath):
    data = load_data(filepath)
    mu = np.average(data)
    sigma = np.std(data)
    cutoff = mu + 2 * sigma
    return round(cutoff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Computes the popularity cutoff (above 2 SD from the mean) of all "
                                                 "Karma scores stored in Karma Scores.csv")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    args = parser.parse_args()
    print compute_cutoff(args.filepath)