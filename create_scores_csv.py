__author__ = 'tracyrohlin'
from os.path import isfile
import os
import csv
from Naive_Bayes_model import extract_karma


def calculate_karma(subreddit, list_of_scores, filename):
        """Creates a csv file of all the scores associated with the requested reddit posts/comments.."""

        csvname = "{} {}.csv".format(subreddit, filename)

        with open(csvname, "ab") as csvfile:
            KarmaWriter = csv.writer(csvfile)
            for score in list_of_scores:
                KarmaWriter.writerow([score])

"""
os_path = "/Users/tracyrohlin/PycharmProjects/RedditCorpus/askwomen/"

scores = []
os.chdir(os_path)
for file in os.listdir("."):
    if isfile(file) and str(file).endswith("txt"):
        scores.append(extract_karma(file))

scores.sort()
calculate_karma("new_learnpython", scores, "Scores")
"""