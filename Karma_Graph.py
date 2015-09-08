#!/usr/bin/env python

__author__ = 'tracyrohlin'
import sys
import glob
import os
import argparse

import matplotlib.pyplot as plt
import numpy as np

def load_data(filepath):
    filepath = filepath
    os.chdir(filepath)
    subreddit = filepath.split("/")[-1]
    filepath += "/*Karma Scores.csv"
    file = glob.glob(filepath)[0]
    data = np.loadtxt(file, delimiter=",", )

    return subreddit, data

def create_graph(filepath, num_of_bins):
    """"Creates a graph of all the Karma scores saved in the csv file.  It takes the directory path where the csv file
    is saved as an argument."""

    subreddit, data = load_data(filepath)
    data.sort()
    hist, bins = np.histogram(data, bins=num_of_bins)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    fig, ax = plt.subplots()
    ax.bar(center, hist, align="center", width=width)

    filename = "{} Karma Scores.png".format(subreddit)
    fig.savefig(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a histogram of the karma scores.")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    parser.add_argument("bins", help='Provide the number of bins to construct the histogram')
    args = parser.parse_args()
    create_graph(args.filepath, int(args.bins))