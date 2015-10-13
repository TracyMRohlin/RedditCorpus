import argparse
import numpy as np
import json
import os

from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from os.path import isfile
from pandas import DataFrame
from pprint import pprint

from text_reader import read_files
from popularity_cutoff import compute_cutoff
from create_LDA import CorpusLDA


POPULAR = "POPULAR"
UNPOPULAR = "UNPOPULAR"

SOURCES = []

def build_data_frame(file, classification):
    rows = []
    index = []
    file_name, text = read_files(file)
    rows.append({'text': text, 'class': classification})
    index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame


def extract_karma(filename):
    """Extracts the karma score from the filename."""
    names = str(filename).split()
    i = names.index('Karma')
    return float(names[i+1])


def classify_initial_data(filepath):
    """Labels the data as popular/not popular based on the cutoff score (which is two SD above the mean)"""
    os.chdir(filepath)
    cutoff = compute_cutoff(filepath)
    for file in os.listdir("."):
        if isfile(file) and str(file).endswith("txt"):
            if extract_karma(file) >= cutoff:
                SOURCES.append((file, POPULAR))
            else:
                SOURCES.append((file, UNPOPULAR))
    return SOURCES


def make_data():
    """Creates the data array and randomly sorts it."""
    data = DataFrame({'text': [], 'class': []})
    for file, classification in SOURCES:
        data = data.append(build_data_frame(file, classification))
    data = data.reindex(np.random.permutation(data.index))
    return data

os.chdir("/Users/tracyrohlin/PycharmProjects/RedditCorpus/fitness")
classify_initial_data(".")
data = make_data()

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(data["text"].values)
#print X_train_counts.shape

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
x_train_tf = tf_transformer.transform(X_train_counts)
#print x_train_tf.shape

clf = MultinomialNB().fit(x_train_tf, data["class"].values)
docs_new = data['text'].values
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(data['class'].values, predicted):
    print doc, category