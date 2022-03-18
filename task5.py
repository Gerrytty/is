import pandas as pd
import numpy as np
from task3 import create_index
from task3 import to_normal_form
from sklearn.metrics.pairwise import cosine_similarity


def tf(vocab, list_of_words):

    tf_matrix = []

    arr = np.zeros(len(vocab))

    for i, word in enumerate(vocab):
        arr[i] = list_of_words.count(word)

    tf_matrix.append(list(map(lambda x: x / len(list_of_words), arr)))

    return np.array(tf_matrix)


def tf_idf(tf, idf):
    tf_idf_matrix = np.zeros((tf.shape[1], tf.shape[0]))

    for word_i, row in enumerate(tf.T):
        for doc_i, column in enumerate(row):
            tf_idf_matrix[word_i][doc_i] = column * idf[word_i]

    return tf_idf_matrix


def search(text):
    list_of_words = to_normal_form(text.lower().split(" "))
    inverse_index = create_index("normal_form_docs")
    set_of_words = list(inverse_index.keys())
    tf_of_search = tf(set_of_words, list_of_words)

    idf = pd.read_csv("idf.csv").to_numpy().T[1]

    tf_idf_of_search = tf_idf(tf_of_search, idf).T[0]

    tf_idf_of_all_docs = pd.read_csv("tf_idf.csv").to_numpy().T

    cosines = list(zip(range(0, 100), cosine_similarity(tf_idf_of_all_docs[1:], tf_idf_of_search.reshape(1, -1)).T[0]))

    # cosines = []
    # for i, tf_doc in enumerate(tf_idf_of_all_docs[1:]):
    #     cosines.append((i, cosine_similarity(tf_doc.reshape(1, -1), tf_idf_of_search.reshape(1, -1))[0][0]))

    return sorted(cosines, key=lambda tup: tup[1], reverse=True)


def get_relevant_docs(text, top_n):
    relevant_docs = search(text)
    return relevant_docs[:top_n]


if __name__ == "__main__":

    text = "научная библиотека"

    print(get_relevant_docs(text, 100))