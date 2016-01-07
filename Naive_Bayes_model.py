#!/usr/bin/env python
__author__ = 'tracyrohlin'

import argparse
import numpy as np
import os

from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import LatentDirichletAllocation

from os.path import isfile
from pandas import DataFrame

from text_reader import read_files
from popularity_cutoff import compute_cutoff

POPULAR = "POPULAR"
UNPOPULAR = "UNPOPULAR"

SOURCES = []
VALIDATION = []
TESTING = []

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


def classify_initial_data(filepath, cutoff, source_type):
    """Labels the data as popular/not popular based on the cutoff score (which is two SD above the mean)"""
    os.chdir(filepath)

    for file in os.listdir("."):
        if isfile(file) and str(file).endswith("txt"):
            if extract_karma(file) >= cutoff:
                source_type.append((file, POPULAR))
            else:
                source_type.append((file, UNPOPULAR))
    return source_type


def make_data(source_type, filepath):
    """Creates the data array and randomly sorts it."""
    print "Creating the data frame."
    os.chdir(filepath)
    data = DataFrame({'text': [], 'class': []})
    for file, classification in source_type:
        data = data.append(build_data_frame(file, classification))
    #data = data.reindex(np.random.permutation(data.index))
    return data


def create_Naive_Bayes(training_data, other_data, topic_type, num_topics):
    """This program is based on the one taught in the tutorial:
    http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html
    written by Zac Stewart."""
    num_topics = int(num_topics)

    confusion = np.array([[0, 0], [0, 0]])
    corpus_length = 0

    # training data remains the same
    train_class = training_data['class'].values.astype(str)
    train_text = training_data['text'].values.astype(str)

    test_text = other_data['text'].values.astype(str)
    test_class = other_data['class'].values.astype(str)
    corpus_length += len(training_data) + len(other_data)

    if topic_type == "tfidf":
        pipeline = Pipeline([('vect', CountVectorizer(min_df=3)),
                        ('tfidf',  TfidfTransformer()),
                        ('clf', MultinomialNB())
                             ])
    elif topic_type == "lda":
        pipeline = Pipeline([('vect', CountVectorizer(min_df=3)),
                        ('lda',  LatentDirichletAllocation(n_topics=num_topics, random_state=1234, max_iter=500, learning_decay=0.5)),
                        ('clf', MultinomialNB())])
    else:
        pipeline = Pipeline([('vect', CountVectorizer(min_df=3)),
                        ('clf', MultinomialNB())
                        ])

    pipeline.fit(train_text, train_class)
    predictions = pipeline.predict(test_text)

    # append to the confusion matrix and score so that later the F1 sccores can be averaged
    confusion += confusion_matrix(test_class, predictions)
    F1score = f1_score(test_class, predictions, pos_label="POPULAR")
    accuracy = accuracy_score(test_class, predictions)

    print 'Total documents classified:', corpus_length
    print "Accuracy: ", accuracy
    print 'F1 Score:', F1score
    print 'Confusion matrix:'
    print confusion

    return F1score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds a Naive Bayes model for classification.")
    parser.add_argument("filepath", help="Argument must be the filepath where the text files are located")
    parser.add_argument("topic_type", help="topic_type is either bow, tfidf or lda")
    parser.add_argument("valid_or_test", help="Either v or t to test against validation or test set")
    parser.add_argument("--num_topics", default=10, help="The amount of topics to be grabbed from the LDA model")
    args = parser.parse_args()

    cutoff = compute_cutoff(args.filepath)

    print "Classifying the initial data."
    classify_initial_data(args.filepath, cutoff, SOURCES)
    training_data = make_data(SOURCES, args.filepath)

    if args.valid_or_test[0].lower() == "v":
        print "Classifying the validation data."
        validation_filepath = args.filepath + "/validation"
        classify_initial_data(validation_filepath, cutoff, VALIDATION)
        validation_data = make_data(VALIDATION, validation_filepath)
        create_Naive_Bayes(training_data, validation_data, args.topic_type, args.num_topics)

    else:
        print "Classifying the testing data."
        testing_filepath = args.filepath + "/testing"
        classify_initial_data(testing_filepath, cutoff, TESTING)
        testing_data = make_data(TESTING, testing_filepath)
        create_Naive_Bayes(training_data, testing_data, args.topic_type, args.num_topics)