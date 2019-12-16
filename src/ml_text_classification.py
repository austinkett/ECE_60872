"""
This file is an attempt to use the comments taken from issues and identify which of them were reproducible and which
weren't based on the choice of words.

Code taken from (Almost exact copy of) tutorial located at:
https://sanjayasubedi.com.np/machinelearning/nlp/text-classification-with-sklearn/
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_files

DATA_DIR = "C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\ml_data_JD"


def main():
    data = load_files(DATA_DIR, encoding="utf-8", decode_error="replace")
    # calculate count of each category
    labels, counts = np.unique(data.target, return_counts=True)
    # convert data.target_names to np array for fancy indexing
    labels_str = np.array(data.target_names)[labels]
    print(dict(zip(labels_str, counts)))

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)
    list(t[:80] for t in X_train[:10])

    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000, decode_error="ignore")
    vectorizer.fit(X_train)

    vectorizer.fit(X_train)
    X_train_vectorized = vectorizer.transform(X_train)

    from sklearn.naive_bayes import MultinomialNB
    cls = MultinomialNB()
    # transform the list of text to tf-idf before passing it to the model
    cls.fit(vectorizer.transform(X_train), y_train)

    from sklearn.metrics import classification_report, accuracy_score

    y_pred = cls.predict(vectorizer.transform(X_test))
    print(accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    main()
