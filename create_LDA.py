#!/usr/bin/env python
__author__ = 'tracyrohlin'
import json
import argparse

from collections import defaultdict
from gensim.models import ldamodel
from create_tfidf import CorpusTFIDF


class CorpusLDA(CorpusTFIDF):
    def __init__(self, filepath, save=False):
        super(CorpusLDA, self).__init__(filepath, save)


    def create_popular_lda_model(self, num_topics, num_words):
        self.create_corpus("popular")
        return self.create_general_lda_model(num_topics, num_words)


    def create_unpopular_lda_model(self, num_topics, num_words):
        self.create_corpus("popular")
        return self.create_general_lda_model(num_topics, num_words)


    def create_general(self, num_topics, num_words):
        self.create_corpus("other")
        return self.create_general_lda_model(num_topics, num_words)


    def create_general_lda_model(self, num_topics, num_words):
        num_topics = int(num_topics)
        num_words = int(num_words)
        lda = ldamodel.LdaModel(corpus=self.corpus, num_topics=num_topics)
        lda_words = []

        i = 1
        data = defaultdict()
        for topics in lda.show_topics(formatted=False, num_words=num_words):
            sub_topic = "Topic # {}".format(i)
            sub_words = []
            for topic in topics:
                prob, wordid = topic
                prob = round(prob, 6)
                wordid = int(wordid)
                actual_word = self.dictionary[wordid]
                lda_words.append(actual_word)
                sub_words.append([actual_word, prob])
            data[sub_topic] = sub_words
            i+=1

        if self.save:
            with open("LDA Model Topics.json", "w") as jsonfile:
                json.dump(data, jsonfile, indent=4, sort_keys=True)
        return " ".join(lda_words)


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
    parser.add_argument("num_topics", help="The amount of topics to estimate")
    parser.add_argument("num_words", help="The amount of words per topic to include in the final result")
    args = parser.parse_args()
    new = CorpusLDA(args.filepath)
    new.read_texts()
    print new.create_general_lda_model(args.num_topics, args.num_words)