#!/usr/bin/env python
__author__ = 'Tracy Rohlin'

import os
import argparse
from reddit_text import RedditText
from create_scores_csv import calculate_karma




def create_post(filepath):
    os.chdir(filepath)
    counter = 0
    for file in os.listdir("."):
        counter +=1
        """if str(file).endswith(".txt"):
            with open(file) as f:
                text = f.read()
                tokenized = RedText.token_and_tag(text)
            with open(file, "w") as f:
                f.write(tokenized)"""
    print "{} documents processed".format(counter)

if __name__ == "__main__":
    RedText = RedditText()
    parser = argparse.ArgumentParser(description="Manually create text files with reddit posts. Useful for link posts")
    parser.add_argument("filepath", help="Enter where the post is to be saved")
    args = parser.parse_args()
    create_post(args.filepath)