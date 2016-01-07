#!/usr/bin/env python
import os
import json
import argparse
import operator
import gensim

from gensim import corpora, models
from text_reader import read_files
from popularity_cutoff import compute_cutoff
from collections import defaultdict, OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint


class CorpusTFIDF(object):


    def __init__(self, wd=None, save=None):
        if wd:
            os.chdir(wd)
            self.reddit = str(wd).split("/")[-2]
            self.cutoff = compute_cutoff(wd)
        self.popular_texts = []
        self.unpopular_texts = []
        self.corpus = []
        self.all_texts = []
        self.save = False
        self.word_counts = defaultdict(int)
        self.vectorizer = None
        if save:
            if save.lower()[0] == "y":
                self.save = True

    def read_texts(self):
        for file in os.listdir("."):
            stuff = read_files(file)
            if not stuff:
                continue
            text = stuff[1].split()
            for word in text:
                self.word_counts[word] +=1
            self.all_texts.append(text)


    def yield_word_vectors(self, pop_type):
        """Yields word vectors later used in the create_tfidf() function"""
        self.dictionary = corpora.Dictionary(pop_type)
        self.dictionary.filter_extremes(no_below=3)

        for text in pop_type:
            yield self.dictionary.doc2bow(text)


    def create_corpus(self, ptype):
        if ptype == "popular":
            self.corpus = list(self.yield_word_vectors(self.popular_texts))
        elif ptype == "unpopular":
            self.corpus = list(self.yield_word_vectors(self.unpopular_texts))
        else:
            self.corpus = list(self.yield_word_vectors(self.all_texts))


    def create_general_tfidf(self, ptype, n):
        self.create_corpus(ptype)
        tfidf = models.TfidfModel(self.corpus, dictionary=self.dictionary)
        top_tfidf_words = defaultdict(list)
        n = int(n)

        # creates a new dictionary object of the top n scored words according to the tfidf model
        for words in self.corpus:
            new_dict = dict(sorted(dict((k, v) for (k, v) in tfidf[words]).items(), key=operator.itemgetter(1), reverse=True)[:n])
            for word_id, score in new_dict.items():
                top_tfidf_words[score].append(self.dictionary[word_id])

        top_tfidf_words = OrderedDict(sorted(top_tfidf_words.items()))

        print "This is how many documents are in the corpus: " + str(len(self.corpus))
        print "This is how many words are in the dictionary: " + str(len(self.dictionary.keys()))
        if self.save:
            filename = "Top {} {} TFIDF Scores.json".format(n, self.reddit)
            with open(filename, "w") as jsonfile:
                json.dump(top_tfidf_words, jsonfile, indent=4, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a model of most popular topic words based on LDA.")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    parser.add_argument("n", help="The top n scored words for each document.")
    parser.add_argument("--save")
    args = parser.parse_args()
    new = CorpusTFIDF(args.filepath, args.save)
    new.read_texts()
    print new.create_general_tfidf("general", args.n)