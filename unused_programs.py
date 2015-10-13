def lda_words():
    """Returns a bag of words that consists entirely of the top n lda words created by create_LDA.py"""
    file_name = "LDA Model Topics.json"
    text = []
    with open(file_name) as jsonfile:
        data = json.load(jsonfile)
        for datum in data:
            for pair in data[datum]:
                text.append(pair[0])
    return text


def bag_of_words():
    """Returns a bag of words out of all the words in the corpus."""
    filepath = raw_input("Where are the training files located?\n")
    text = []
    for file in os.listdir(filepath):
        if str(file).endswith(".txt"):
            text.append("".join(read_files(file)[1]))
    return text