import os

from os.path import isfile, join

DEMARCATORS = ['==============================',
               'Title:', 'New post:', 'Comments from post:']

def read_files(file):
    if str(file).endswith(".txt"):
        with open(file) as f:
            text = f.read()

            for dm in DEMARCATORS:
                text = text.replace(dm, "")# removes all of the demarcations between posts/comments
            list_of_words = text.split()
            if "Karma:" in list_of_words:
                i = list_of_words.index('Karma:') # removes the score and word "Karma" so it doesn't influence TF-IDF scores
                del list_of_words[i:i+2]
            if "Date:" in list_of_words:
                i = list_of_words.index("Date:")
                del list_of_words[i:i+2]
        text = " ".join(list_of_words)

        return file, text