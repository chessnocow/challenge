"""Twitter helpers."""

from collections import Counter
from const import CHECK_POINTS, SENTIMENT_THRESHOLD
from dbase import get_total_number_of_tweets, get_tweets_from_db
from sentiment import get_sentiment

import os
import pandas as pd
import tweepy


def get_twitter_client(bearer_token=None):
    """
    Get twitter client instance.

    :param bearer_token: bearer token to authorize, if None then take the token from environment variable BEARER_TOKEN
    :return: twitter client instance
    """
    bearer_token = bearer_token or os.environ.get("BEARER_TOKEN")
    return tweepy.Client(bearer_token)


def get_users_dict(users):
    """
    Convert list of tweepy.Users object to dictionary.

    Key is the user_id, value is the username.
    :param users:
    :return: dictionary of names to ids
    """
    return {user.id: user.username for user in users} if users else None


def get_tweets_df(client, query, start_time):
    """
    Get pd.DataFrame of tweets searched by query since the start_time.

    :param client: tweeter client instance
    :param query: string to search
    :param start_time: start time for tweets search (couldn't be more than 7 days before the current date)
    :return: pandas DataFrame with data about tweets
    """
    columns = ["search_query", "tweet_id", "user_id", "username", "created_at", "text", "sentiment_polarity"]
    results_dict = {col: [] for col in columns}
    next_token = None
    # loop for pagination
    while True:
        results = client.search_recent_tweets(
            query,
            max_results=100,
            tweet_fields=["author_id", "created_at", "text", "lang"],
            user_fields=["name", "username"],
            expansions=["author_id"],
            start_time=start_time,
            next_token=next_token,
        )
        users = get_users_dict(results.includes.get("users"))
        if not results.data:
            return pd.DataFrame()
        for tweet in results.data:
            results_dict["search_query"].append(query)
            results_dict["tweet_id"].append(tweet.id)
            results_dict["user_id"].append(tweet.author_id)
            results_dict["username"].append(users.get(tweet.author_id))
            results_dict["created_at"].append(tweet.created_at)
            results_dict["text"].append(tweet.text)
            results_dict["sentiment_polarity"].append(get_sentiment(tweet.text)[0])
        next_token = results.meta.get("next_token")
        if not next_token:
            # exit the loop
            break
    return pd.DataFrame(results_dict)


def get_top_tweeps(tweets):
    """
    Get top 10 (or less) authors.

    :param tweets: list of tweets (lists)
    :return: sorted list of tuples ('username', number_of_tweets)
    """
    authors = Counter()
    for tweet in tweets:
        authors[tweet[3]] += 1
    return authors.most_common(10)


def get_average_sentiment(tweets):
    """
    Calculate average sentiment polarity.

    :param tweets: list of tweets (lists)
    :return: polarity as a string according to the calculated average
    """
    if not tweets:
        return None
    polarity = 0
    for tweet in tweets:
        polarity += tweet[6]
    average_polarity = polarity / len(tweets)
    return (
        "negative"
        if average_polarity < -SENTIMENT_THRESHOLD
        else "positive"
        if average_polarity > SENTIMENT_THRESHOLD
        else "neutral"
    )


def print_metrics(check_time, query):
    """
    Print metrics for the particular time and query.

    :param check_time: datetime object
    :param query: the query to search
    :return: None
    """
    tweets = get_tweets_from_db(check_time, query)
    print(f"Metrics for query: {query}")
    print(f"Total number of tweets matching the query seen so far: {get_total_number_of_tweets(query)}")
    for n_min in CHECK_POINTS:
        print(f"Tweets for last {n_min} minute{'s' if n_min > 1 else ''}: {len(tweets[n_min])}")
    for n_min in CHECK_POINTS:
        if not tweets[n_min]:
            continue
        print(f"Top tweeps for last {n_min}  minute{'s' if n_min > 1 else ''}:")
        top_tweeps = get_top_tweeps(tweets[n_min])
        for place, tweep in enumerate(top_tweeps):
            print(f"\t{tweep[0]} with {tweep[1]} tweets.")
    for n_min in CHECK_POINTS:
        if not tweets[n_min]:
            continue
        print(
            f"The polarity of tweets for last {n_min}  minute{'s' if n_min > 1 else ''} "
            f"was {get_average_sentiment(tweets[n_min])}"
        )
