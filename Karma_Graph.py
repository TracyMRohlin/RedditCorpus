#!/usr/bin/env python

__author__ = 'tracyrohlin'
import glob
import os
import argparse

import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def load_data(filepath):
    os.chdir(filepath)
    file = glob.glob("*Scores.csv")[0]
    data = np.loadtxt(file, delimiter=",", )
    return data

def create_graph(filepath, subreddit, num_of_bins):
    """"Creates a graph of all the Karma scores saved in the csv file.  It takes the directory path where the csv file
    is saved as an argument."""
    os.chdir(filepath)
    data = load_data(filepath)
    data.sort()
    hist, bins = np.histogram(data, bins=num_of_bins)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    fig, ax = plt.subplots()
    ax.bar(center, hist, align="center", width=width)
    ax.set_title("Karma Scores from {}".format(subreddit.capitalize()))

    filename = "{} Karma Scores.png".format(subreddit)
    fig.savefig(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a histogram of the karma scores.")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    parser.add_argument("subreddit", help="Name of the subreddit from which the Karma came from")
    parser.add_argument("bins", help='Provide the number of bins to construct the histogram')
    args = parser.parse_args()
    create_graph(args.filepath, args.subreddit, int(args.bins))