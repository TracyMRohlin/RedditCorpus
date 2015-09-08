import os
import csv
import re

from collections import defaultdict
from pprint import pprint
from gensim import corpora, models
from os.path import isfile, join



class CorpusStats:


    def __init__(self):
        wd = raw_input("Please enter the filepath where the corpus files are located:\n")
        os.chdir(wd)
        self.texts = []
        self.all_scores = []
        DEMARCATORS = ['==============================',
               'Title:', 'New post:', 'Comments from post:']

        # The purpose of self.num_of_docs is further explained in create_tfidf()
        self.num_of_docs = 0
        for file in os.listdir("."):
            if isfile(join(os.curdir,file)) and file.endswith("txt"):
                self.num_of_docs += 1
                with open(file) as f:
                    text = f.read()

                    for dm in DEMARCATORS:
                        text = text.replace(dm, "")# removes all of the demarcations between posts/comments
                    list_of_words = text.split()
                    if "Karma:" in list_of_words:
                        i = list_of_words.index('Karma:') # removes the score and word "Karma" so it doesn't influence TF-IDF scores
                        del list_of_words[i:i+1]

                    self.texts.append(list_of_words)


    def create_dictionary(self):
        """Creates a word frequency dictionary that can be opened using dictionary.token2id"""

        self.dictionary = corpora.Dictionary(self.texts)
        filepath = os.curdir + "words.dict"
        self.dictionary.save(filepath)


    def yield_word_vectors(self):
        self.create_dictionary()
        for text in self.texts:
            yield self.dictionary.doc2bow(text)


    def create_tfidf(self):
        corpus = list(self.yield_word_vectors())
        #filepath = "corpus.mm"
        corpora.MmCorpus.serialize("corpus.mm", corpus)
        tfidf = models.TfidfModel(corpus, dictionary=self.dictionary)
        tfidf_dict = defaultdict()

        for k, v in self.dictionary.items():
            new_dict = {"word": v, "tfidf": []}
            tfidf_dict[k] = new_dict

        i = 0
        for words in corpus:
            for word in tfidf[words]:
                word_id, t_score = word
                tfidf_dict[word_id]["tfidf"].append(round(t_score, 3))

            i+=1

        print "this is how many items are in the corpus: " + str(len(corpus))
        print "this is how many documents are in the model : " + str(i)
        print "this is how many words are in the dictionary: " + str(len(self.dictionary.keys()))

        self.create_csv("tfidf", tfidf_dict)




    def create_csv(self, modeltype, dictobject):
        """Creates a csv file based on the objects in the tf-idf/lda model).  It takes the modeltype (tf-idf or LDA)
        and the dictionary where the scores are stored as arguments."""

        filename = "{} Scores.csv".format(modeltype)
        with open(filename, "wb") as f:
            modelwriter = csv.writer(f)
            for word_id in dictobject.keys():
                word = dictobject[word_id]["word"].encode('utf8')
                scores = dictobject[word_id][modeltype]
                out = [word_id, word]+scores
                modelwriter.writerow(out)



if __name__ == "__main__":
    new = CorpusStats()
    new.create_tfidf()

