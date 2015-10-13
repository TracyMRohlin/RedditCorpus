#!/usr/bin/env python
import os
import json
import argparse
import operator

from collections import defaultdict
from gensim import corpora, models
from text_reader import read_files
from create_data_array import extract_karma
from popularity_cutoff import compute_cutoff

import pdb
from pprint import pprint
#pdb.set_trace()


class CorpusTFIDF(object):


    def __init__(self, wd, save=False):
        os.chdir(wd)
        self.popular_texts = []
        self.unpopular_texts = []
        self.corpus = []
        self.all_texts = []
        DEMARCATORS = ['==============================',
               'Title:', 'New post:', 'Comments from post:']
        self.cutoff = compute_cutoff(wd)
        self.save = False
        if save == "True":
            self.save = True

    def read_texts(self):
        for file in os.listdir("."):
            stuff = read_files(file)
            if not stuff:
                continue
            text = stuff[1].split()
            self.all_texts.append(text)


    def yield_word_vectors(self, pop_type):
        """Yields word vectors later used in the create_tfidf() function"""
        self.dictionary = corpora.Dictionary(pop_type)

        for text in pop_type:
            yield self.dictionary.doc2bow(text)


    def create_corpus(self, ptype):
        if ptype == "popular":
            self.corpus = list(self.yield_word_vectors(self.popular_texts))
        elif ptype == "unpopular":
            self.corpus = list(self.yield_word_vectors(self.unpopular_texts))
        else: self.corpus = list(self.yield_word_vectors(self.all_texts))


    def create_general_tfidf(self, ptype, n):
        self.create_corpus(ptype)
        tfidf = models.TfidfModel(self.corpus, dictionary=self.dictionary)
        tfidf_dict = {}
        top_tfidf_words = []

        # creates a new dictionary object of the top n scored words according to the tfidf model
        for words in self.corpus:
            new_dict = dict(sorted(dict((k, v) for (k, v) in tfidf[words]).items(), key=operator.itemgetter(1), reverse=True)[:n])
            tfidf_dict.update(new_dict.items())
            for word_id in new_dict.keys():
                top_tfidf_words.append(self.dictionary[word_id])

        #print "This is how many documents are in the corpus: " + str(len(self.corpus))
        #print "This is how many words are in the dictionary: " + str(len(self.dictionary.keys()))
        if self.save:
            self.create_json("tfidf", tfidf_dict, n)

        return " ".join(top_tfidf_words)





    def create_json(self, modeltype, dictobject, n):
        """Creates a csv file based on the objects in the tf-idf/lda model).  It takes the modeltype (tf-idf or LDA)
        and the dictionary where the scores are stored as arguments."""

        filename = "Top {} {} Scores.json".format(n, modeltype)
        data = []
        for word_id in dictobject.keys():
            word = self.dictionary[word_id].encode('utf8')
            score = dictobject[word_id]
            out = [word_id, word, score]
            data.append(out)
        if self.save:
            with open(filename, "w") as jsonfile:
                json.dump(data, jsonfile, indent=4, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a model of most popular topic words based on LDA.")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    parser.add_argument("n", help="The top n scored words for each document.")
    parser.add_argument("--save")
    args = parser.parse_args()
    new = CorpusTFIDF(args.filepath, args.save)
    new.read_texts()
    new.create_general_tfidf("general", args.n)