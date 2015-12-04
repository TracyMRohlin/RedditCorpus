#!/usr/bin/env python
import time
from SVM_model import *

time1 = time.time()

def average_models(training_data, testing_data, model_type, topic_type, num_topics):
    results = []
    if model_type.lower()[0] == "s":
        for _ in xrange(5):
            score = create_SVM(training_data, testing_data, topic_type, num_topics)
            results.append(score)
    else:
        for _ in xrange(5):
            score = create_Naive_Bayes(training_data, testing_data, topic_type, num_topics)
            results.append(score)
    return sum(results) / len(results)

def create_data(filepath, model_type, topic_type, v_or_t, num_topics):
    print "Classifying the initial data."
    cutoff = compute_cutoff(filepath)
    classify_initial_data(filepath, cutoff, SOURCES)
    training_data = make_data(SOURCES, filepath)
    score = 0

    if v_or_t[0].lower() == "v":
        print "Classifying the validation data."
        validation_filepath = filepath + "/validation"
        classify_initial_data(validation_filepath, cutoff,  VALIDATION)
        validation_data = make_data(VALIDATION, validation_filepath)
        score += average_models(training_data, validation_data, model_type, topic_type, num_topics)
    else:
        print "Classifying the testing data."
        testing_filepath = filepath + "/testing"
        classify_initial_data(testing_filepath, cutoff, TESTING)
        testing_data = make_data(TESTING, testing_filepath)
        score += average_models(training_data, testing_data, model_type, topic_type, num_topics)

    print "Total average for five trials: ", score
    time2 = time.time()
    print "Minutes passed: ", ((time2-time1)/ 60)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds a Naive Bayes model for classification.")
    parser.add_argument("filepath", help="Argument must be the filepath where the text files are located")
    parser.add_argument("model_type", help="model_type is either nb or svm")
    parser.add_argument("topic_type", help="topic_type is either bow, tfidf or lda")
    parser.add_argument("valid_or_test", help="Either v or t to test against validation or test set")
    parser.add_argument("--num_topics", default=10, help="The amount of topics to be grabbed from the LDA model")
    args = parser.parse_args()
    create_data(args.filepath, args.model_type, args.topic_type, args.valid_or_test, args.num_topics)