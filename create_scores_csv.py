__author__ = 'tracyrohlin'

import csv
from math import log

def calculate_karma(subreddit, list_of_scores, filename):
        """Creates a csv file of all the scores associated with the requested reddit posts/comments.."""

        csvname = "{} {}.csv".format(subreddit, filename)

        with open(csvname, "ab") as csvfile:
            KarmaWriter = csv.writer(csvfile)
            for score in list_of_scores:
                KarmaWriter.writerow([score])



