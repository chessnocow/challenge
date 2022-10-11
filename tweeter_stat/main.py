"""Twitter metrics app."""

from const import DB_NAME, REFRESH_API_DATA_SECONDS, REFRESH_METRICS_SECONDS, TABLE_NAME
from datetime import datetime, timedelta
from twitter import get_tweets_df, get_twitter_client, print_metrics

import sqlite3
import sys


def main(query):
    """
    Get and print Twitter metrics.

    :param query: query to search
    :return: None
    """
    client = get_twitter_client()
    start_time = datetime.utcnow() - timedelta(minutes=15)
    last_check_time = datetime.utcnow()
    while True:
        if datetime.utcnow() - start_time > timedelta(seconds=REFRESH_API_DATA_SECONDS):
            tweets_df = get_tweets_df(client, query, start_time)
            start_time = datetime.utcnow()
            with sqlite3.connect(DB_NAME) as conn:
                tweets_df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        if datetime.utcnow() - last_check_time > timedelta(seconds=REFRESH_METRICS_SECONDS):
            print("Updating metrics...\n\n")
            print(f"Updated {datetime.now()}")
            last_check_time = datetime.utcnow()
            print_metrics(last_check_time, query)
            print("Press Ctrl+C to quit")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "Kahoot"
    main(query)
