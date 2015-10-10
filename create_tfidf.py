#!/usr/bin/env python
import os
import json
import argparse

from collections import defaultdict
from gensim import corpora, models
from text_reader import read_files
from create_data_array import extract_karma
from popularity_cutoff import compute_cutoff

import pdb
from pprint import pprint
#pdb.set_trace()


class CorpusTFIDF(object):


    def __init__(self, wd, save):
        os.chdir(wd)
        self.popular_texts = []
        self.unpopular_texts = []
        self.corpus = []
        self.all_texts = self.unpopular_texts.extend(self.unpopular_texts)
        DEMARCATORS = ['==============================',
               'Title:', 'New post:', 'Comments from post:']
        self.cutoff = compute_cutoff(wd)
        self.save = save

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


    def create_tfidf(self, ptype):
        self.create_corpus(ptype)
        corpora.MmCorpus.serialize("corpus.mm", self.corpus)
        tfidf = models.TfidfModel(self.corpus, dictionary=self.dictionary)
        tfidf_dict = defaultdict()

        # creates a new dictionary object so that the tfidf scores and words can be be saved per row in a csv file
        for k, v in self.dictionary.items():
            new_dict = {"word": v, "tfidf": []}
            tfidf_dict[k] = new_dict

        for words in self.corpus:
            for word in tfidf[words]:
                word_id, t_score = word
                tfidf_dict[word_id]["tfidf"].append(round(t_score, 3))


        print "This is how many documents are in the corpus: " + str(len(self.corpus))
        print "This is how many words are in the dictionary: " + str(len(self.dictionary.keys()))

        self.create_json("tfidf", tfidf_dict)




    def create_json(self, modeltype, dictobject):
        """Creates a csv file based on the objects in the tf-idf/lda model).  It takes the modeltype (tf-idf or LDA)
        and the dictionary where the scores are stored as arguments."""

        filename = "{} Scores.json".format(modeltype)
        data = []
        for word_id in dictobject.keys():
            word = dictobject[word_id]["word"].encode('utf8')
            scores = dictobject[word_id][modeltype]
            out = [[word_id, word]+scores]
            data.append(out)
        if self.save:
            with open(filename, "w") as jsonfile:
                json.dump(data, jsonfile, indent=4, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a model of most popular topic words based on LDA.")
    parser.add_argument("filepath", help="Argument must be the filepath where the KarmaScores.csv file is located")
    parser.add_argument("--save")
    args = parser.parse_args()
    new = CorpusTFIDF(args.filepath, args.save)
    new.read_texts()