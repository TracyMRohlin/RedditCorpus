#!/usr/bin/env python
__author__ = 'tracyrohlin'

import argparse
import numpy as np
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
from create_tfidf import CorpusTFIDF


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
    print "Classifying the initial data."
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
    print "Creating the data frame."
    data = DataFrame({'text': [], 'class': []})
    for file, classification in SOURCES:
        data = data.append(build_data_frame(file, classification))
    data = data.reindex(np.random.permutation(data.index))
    return data


def create_mini_tfidf(texts, labels, num_words):
    """Creates a single string of all the top n tfidf-scored words
     based on the kth fold training and testing data."""
    num_words = int(num_words)
    textList =[]
    new = CorpusTFIDF(".")
    for i, label in enumerate(texts):
        if label == "POPULAR":
            new.popular_texts.append(texts[i].split())
        else: new.popular_texts.append(texts[i].split())
    popular = new.create_general_tfidf("popular", num_words)
    unpopular = new.create_general_tfidf("unpopular", num_words)
    for label in labels:
        if label == "POPULAR":
            textList.append(popular)
        else: textList.append(unpopular)
    return np.array(texts)



def create_mini_LDA(texts, labels, num_topics, num_words):
    """Creates a miniature LDA model based on the kth fold training and testing data."""
    num_topics = int(num_topics); num_words = int(num_words)
    textList =[]
    new = CorpusLDA(".")
    for i, label in enumerate(texts):
        if label == "POPULAR":
            new.popular_texts.append(texts[i].split())
        else: new.popular_texts.append(texts[i].split())
    popular = new.create_popular_lda_model(num_topics, num_words)
    unpopular = new.create_unpopular_lda_model(num_topics, num_words)
    for label in labels:
        if label == "POPULAR":
            textList.append(popular)
        else: textList.append(unpopular)
    return np.array(texts)


def create_Naive_Bayes(topic_type, num_topics, num_words):
    """This program is based on the one taught in the tutorial:
    http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html
    written by Zac Stewart."""

    pipeline = Pipeline([
        ('count_vectorizer',   CountVectorizer()),
        ('classifier',         MultinomialNB())
        ])

    k_fold = KFold(n=len(data), n_folds=6)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])
    # randomly grabs certain texts and splits them into training and testing sections, then runs the model of choice
    i = 1
    for train_indices, test_indices in k_fold:
        print "In fold # {}".format(i)
        i+=1
        train_class = data.iloc[train_indices]['class'].values.astype(str)
        train_text = data.iloc[train_indices]['text'].values.astype(str)

        test_text = data.iloc[test_indices]['text'].values
        test_class = data.iloc[test_indices]['class'].values.astype(str)

        if topic_type == "lda":
            print "Creating latent dirichlet allocation model on the data. Please wait..."
            train_text = create_mini_LDA(train_text,train_class, num_topics, num_words)
            test_text = create_mini_LDA(test_text, test_class, num_topics, num_words)
        elif topic_type == "tfidf":
            print "Creating tfidf model on the data. Please wait."
            train_text = create_mini_tfidf(train_text,train_class, num_words)
            test_text = create_mini_tfidf(test_text, test_class, num_words)
        else: pass


        pipeline.fit(train_text, train_class)
        predictions = pipeline.predict(test_text)

        # append to the confusion matrix and score so that later the F1 sccores can be averaged
        confusion += confusion_matrix(test_class, predictions)
        score = f1_score(test_class, predictions, pos_label=POPULAR)
        scores.append(score)
        #for label, predict in zip(test_class, predictions):
         #   print label, predict

    print 'Total documents classified:', len(data)
    print 'Score:', sum(scores)/len(scores)
    print 'Confusion matrix:'
    print confusion


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds a Naive Bayes model for classification.")
    parser.add_argument("filepath", help="Argument must be the filepath where the text files are located")
    parser.add_argument("topic_type", help="topic_type is either bow, tfidf or lda")
    parser.add_argument("--num_topics", default=10, help="The amount of topics to be grabbed from the LDA model")
    parser.add_argument("--num_words", default=10, help="The amount of words per topic to be returned")
    args = parser.parse_args()
    os.chdir(args.filepath)
    classify_initial_data(".")
    data = make_data()
    create_Naive_Bayes(args.topic_type, args.num_topics, args.num_words)