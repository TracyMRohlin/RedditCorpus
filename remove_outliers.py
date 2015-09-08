#!/usr/bin/env python
__author__ = 'tracyrohlin'

import os

from fences import fences
from create_scores_csv import calculate_karma

def remove_outliers(filepath):
    """Removes the posts/comments that have scores above and below the upper and lower fences, respectively.
    Also creates a new Karma Scores.csv file """

    lower, upper = fences(filepath)
    list_of_new_scores = []

    i = 0
    os.chdir(filepath)
    for file in os.listdir("."):
        if file.endswith(".txt"):
            names = str(file).split()
            score_index = names.index("Karma") + 1
            score = int(names[score_index])
            if score < lower or score > upper:
                i+=1
                os.remove(file)
            else:
                list_of_new_scores.append(score)
    print "A total of {} outliers were removed from the corpus".format(i)

    subreddit = filepath.split("/")[-1]
    calculate_karma(subreddit, list_of_new_scores, "temp Karma Scores")
    temp_file = "{} temp Karma Scores.csv".format(subreddit)
    new_file = "{} Karma Scores.csv".format(subreddit)
    os.rename(temp_file, new_file)





print remove_outliers("/Users/tracyrohlin/PycharmProjects/RedditCorpus/fitness")