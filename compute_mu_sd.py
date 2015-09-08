#!/usr/bin/env python

__author__ = 'tracyrohlin'

import sys
import argparse
import numpy as np

from Karma_Graph import load_data

def compute_mu_sd(filepath):
    data = load_data(filepath)[1]
    mu = np.average(data)
    sigma = np.std(data)
    return round(mu, 2), round(sigma, 2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Computes the mean and standard deviation of all Karma scores stored"
                                                 "in Karma Scores.csv")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    args = parser.parse_args()
    print compute_mu_sd(args.filepath)