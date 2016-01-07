#!/usr/bin/env python
from Naive_Bayes_model import *
from pprint import pprint

def print_top_TFIDF(dataset, n_top_words):
    n_top_words = int(n_top_words)
    vectorizer = CountVectorizer(min_df=3)
    word_vectors = vectorizer.fit_transform(dataset)
    end_words = ""
    model = LatentDirichletAllocation(n_topics=n_top_words,random_state=1234, max_iter=500, learning_decay=0.5)

    feature_names = vectorizer.get_feature_names()
    model.fit(word_vectors)
    for topic_idx, topic in enumerate(model.components_):
        end_words += "Topic #%d: " % topic_idx
        end_words += " ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]])
        end_words += "\n"


    return end_words





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds a Naive Bayes model for classification.")
    parser.add_argument("filepath", help="Argument must be the filepath where the text files are located")
    parser.add_argument("n", help="How many topics to show")
    parser.add_argument("--save", help="Save the items to a log")
    args = parser.parse_args()


    print "Classifying the initial data."
    classify_initial_data(args.filepath, 0, SOURCES)
    data = make_data(SOURCES, args.filepath)
    text = data['text'].values.astype(str)

    top_lda = print_top_TFIDF(text, args.n)
    print top_lda

    if args.save:
        reddit = args.filepath.split("/")[-2]
        file_name = "{} Top {} LDA words.log".format(reddit, args.n)
        with open(file_name, "w") as f:
            f.write(top_lda)
