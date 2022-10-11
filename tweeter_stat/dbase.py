"""Database SQLite3 helpers."""

from const import CHECK_POINTS, DB_NAME, TABLE_NAME
from datetime import datetime, timedelta
from sqlite3 import Error

import sqlite3


def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file.

    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement.

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: None
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_tweets_for_last_minutes(conn, n, check_time, query):
    """
    Query database for tweets with the particular query for last n minutes.

    :param conn: connection to database
    :param n: number of minutes
    :param check_time: the initial time to calculate the time range
    :param query: query to search for
    :return: list of rows as lists according to the DB schema
    ['search_query', 'tweet_id', 'user_id', 'username', 'created_at', 'text', 'sentiment_polarity']
    """
    start_time = check_time - timedelta(minutes=n)
    return conn.execute(
        f"select distinct * from {TABLE_NAME} where "
        f"unixepoch(created_at) > {(start_time - datetime(1970, 1, 1)).total_seconds()} "
        f"and search_query = '{query}'"
    ).fetchall()


def get_total_number_of_tweets(query):
    """
    Query database for total number of records with the particular query.

    :param query: query to search for
    :return: number of tweets
    """
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute(
            f"select count(distinct tweet_id) from {TABLE_NAME} " f"where search_query = '{query}'"
        ).fetchall()
    return result[0][0]


def get_tweets_from_db(check_time, query):
    """
    Get list of tweets from SQL DB.

    :param check_time: datetime object of the initial time
    :param query: query to search for
    :return: list of rows as lists according to the DB schema
    ['search_query', 'tweet_id', 'user_id', 'username', 'created_at', 'text', 'sentiment_polarity']
    """
    tweets = {}
    with sqlite3.connect(DB_NAME) as conn:
        for n_min in CHECK_POINTS:
            tweets[n_min] = get_tweets_for_last_minutes(conn, n_min, check_time, query)
    return tweets
