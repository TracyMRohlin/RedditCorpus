import os
import shutil
from pprint import pprint
from random import shuffle
from Naive_Bayes_model import extract_karma

oldfilepath = "/Users/tracyrohlin/PycharmProjects/RedditCorpus_copy/learnprogramming/popular/"


onlyfiles = [f for f in os.listdir(oldfilepath) if str(f).endswith(".txt")]
shuffle(onlyfiles)
limit = int(round(len(onlyfiles) * 0.2))

"""for file in onlyfiles:
    if extract_karma(file) >= 22:
        old = oldfilepath + file
        new = "/Users/tracyrohlin/PycharmProjects/RedditCorpus_copy/learnprogramming/popular/" + file
        shutil.move(old, new)"""

for _ in xrange(limit):
    file = onlyfiles[0]
    old = oldfilepath + file
    new = "/Users/tracyrohlin/PycharmProjects/RedditCorpus_copy/learnprogramming/validation/" + file
    shutil.move(old, new)
    del onlyfiles[0]

for _ in xrange(limit):
    file = onlyfiles[0]
    old = oldfilepath + file
    new = "/Users/tracyrohlin/PycharmProjects/RedditCorpus_copy/learnprogramming/testing/" + file
    shutil.move(old, new)
    del onlyfiles[0]