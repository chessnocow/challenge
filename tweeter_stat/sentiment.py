"""Sentiment helpers."""

from textblob import TextBlob


def get_sentiment(text):
    """
    Get sentiment of the text.

    Get average polarity and subjectivity of sentences in the input text.
    :param text: text to analyze
    :return: Tuple of polarity and subjectivity
    """
    blob = TextBlob(text)
    polarity = []
    subjectivity = []
    for sentence in blob.sentences:
        polarity.append(sentence.sentiment.polarity)
        subjectivity.append(sentence.sentiment.subjectivity)
    mean_polarity = sum(polarity) / len(polarity)
    mean_subjectivity = sum(subjectivity) / len(subjectivity)
    return mean_polarity, mean_subjectivity
