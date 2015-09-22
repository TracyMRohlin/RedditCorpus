#!/usr/bin/env python
__author__ = 'tracyrohlin'

import os
import csv
import argparse

def create_csv(filepath):
    os.chdir(filepath)
    with open("Karma split scores.csv", "wb") as f:
        csvwriter = csv.writer(f)


        for file in os.listdir("."):
            if file.endswith(".txt"):
                names = str(file).split()
                score_index = names.index("Karma") + 1
                score = int(names[score_index])
                csvwriter.writerow([score])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a new Karma Scores CSV file based on the split training/testing set")
    parser.add_argument("filepath", help="Argument must be the filepath where the corpus files are located")
    args = parser.parse_args()
    create_csv(args.filepath)