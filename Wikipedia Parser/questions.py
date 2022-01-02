import nltk
import sys
import os
import string
from math import log10

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    while True:
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Exit query
        if len(query) == 1 and (list(query)[0] == "x" or list(query)[0] == "exit"):
            print("See you later!") 
            sys.exit()

        # Invalid question
        elif len(query) == 0: 
            print("Please enter a valid question.")
        else:
            # Determine top file matches according to TF-IDF
            filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

            # Extract sentences from top files
            sentences = dict()
            for filename in filenames:
                for passage in files[filename].split("\n"):
                    for sentence in nltk.sent_tokenize(passage):
                        tokens = tokenize(sentence)
                        if tokens:
                            sentences[sentence] = tokens

            # Compute IDF values across sentences
            idfs = compute_idfs(sentences)

            # Determine top sentence matches
            matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
            for match in matches:
                print(match)


def load_files(directory):
    """
    Given a directory name, returns a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus_dict = {}

    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name), encoding="utf-8") as f:
            corpus_dict[file_name] = f.read()
    
    return corpus_dict


def tokenize(document):
    """
    Given a document, returns a list of all of the
    words in that document, in order.
    Processes document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    words = nltk.word_tokenize(document.lower())
    
    return [w for w in words if w not in punctuation and w not in stopwords] 


def compute_idfs(documents):
    """
    Given a dictionary of `documents`, maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents is in the
    resulting dictionary.
    """
    word_idfs = {}
    doc_list = [] # list for indexing docs
    N = len(documents) # total num of docs
    df = 0 # num of docs containing word
    
    for doc in documents:
        doc_list.append(doc)
    
    for doc in documents:
        for word in documents[doc]:
            for i in range(N):
                if word in documents[doc_list[i]]:
                    df += 1
            idf = log10(N / df)
            word_idfs[word] = idf
            df = 0

    return word_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), returns a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    doc_tfidf = {}

    for doc in files:
        doc_tfidf[doc] = 0
        for word in query:
            if word in idfs:
                doc_tfidf[doc] += files[doc].count(word) * idfs[word]
    
    # extract document key for each item in a dict sorted by tf-idf
    return [key for key,value in sorted(doc_tfidf.items(), key=lambda kv: kv[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), returns a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference is 
    given to sentences that have a higher query term density.
    """
    top_matches = []

    for sent in sentences:
        sent_metrics = [sent, 0, 0] # [sentence, matching word measure, query term density]
        for word in query:
            if word in sentences[sent]:
                sent_metrics[1] += idfs[word]
                sent_metrics[2] += sentences[sent].count(word) / len(sentences[sent])
        top_matches.append(sent_metrics)
    
    # extract sentence element from each item in a list sorted by matching word measure, then by query term density
    return [sent for sent, m1, m2 in sorted(top_matches, key=lambda kv: (kv[1], kv[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
