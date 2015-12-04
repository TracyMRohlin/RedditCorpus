#!/usr/bin/env python
__author__ = 'tracyrohlin'
from Naive_Bayes_model import *
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

POPULAR = "POPULAR"
UNPOPULAR = "UNPOPULAR"

SOURCES = []


def create_SVM(training_data, other_data, topic_type, num_topics):
    """This program is based on the one taught in the tutorial:
    http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html
    written by Zac Stewart."""
    num_topics = int(num_topics)
    if topic_type == "tfidf":

        pipeline = Pipeline([('vect', CountVectorizer(min_df=3)),
                        ('tfidf',  TfidfTransformer()),
                        ('clf', SGDClassifier(random_state=1234, n_iter=2000, alpha=0.009, loss="log"))
                        ])
    elif topic_type == "lda":
        pipeline = Pipeline([('vect', TfidfVectorizer(min_df=3)),
                        ('lda',  LatentDirichletAllocation(n_topics=num_topics, random_state=1234, max_iter=500)),
                        ('clf', SGDClassifier(alpha=0.3,random_state=1234, n_iter=2000, loss="log"))
                             ])
    else:
        pipeline = Pipeline([('vect', CountVectorizer(min_df=3)),
                        ('clf',
                            SGDClassifier(random_state=1234, n_iter=2000, alpha=1.6, loss="log"))
                        ])

    confusion = np.array([[0, 0], [0, 0]])
    corpus_length = 0

    # training data remains the same
    train_class = training_data['class'].values.astype(str)
    train_text = training_data['text'].values.astype(str)

    test_text = other_data['text'].values.astype(str)
    test_class = other_data['class'].values.astype(str)
    corpus_length += len(training_data) + len(other_data)


    pipeline.fit(train_text, train_class)
    predictions = pipeline.predict(test_text)

    # append to the confusion matrix and score so that later the F1 sccores can be averaged
    confusion += confusion_matrix(test_class, predictions)
    score = f1_score(test_class, predictions, pos_label="POPULAR")

    print 'Total documents classified:', corpus_length
    print 'Score:', score
    print 'Confusion matrix:'
    print confusion

    return score



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds a Naive Bayes model for classification.")
    parser.add_argument("filepath", help="Argument must be the filepath where the text files are located")
    parser.add_argument("topic_type", help="topic_type is either bow, tfidf or lda")
    parser.add_argument("valid_or_test", help="Either v or t to test against validation or test set")
    parser.add_argument("--num_topics", default=10, help="The amount of topics to be grabbed from the LDA model")
    parser.add_argument("--num_words", default=10, help="The amount of words per topic to be returned")
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
        create_SVM(training_data, validation_data, args.topic_type, args.num_topics)

    else:
        print "Classifying the testing data."
        testing_filepath = args.filepath + "/testing"
        classify_initial_data(testing_filepath, cutoff, TESTING)
        testing_data = make_data(TESTING, testing_filepath)
        create_SVM(training_data, testing_data, args.topic_type, args.num_topics)