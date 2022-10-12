# Task
Create a proof-of-concept for a tool that allows the user to specify a search term and receive every five seconds an updated output of some metrics about tweets that contain the search term.

The specific insights the tool should provide in its output are:
- What is the total count of tweets matching the search term seen so far?
- How many tweets containing the search term were there in the last 1, 5 and 15 minutes?
- What are the ten most frequent terms (excluding the search term) that appear in tweets containing the search term over the last 1, 5 and 15 minutes?
- Within tweets matching the search term, who were the top ten tweeps (Twitter users) who tweeted the most in the last 1, 5 and 15 minutes?
- What is the sentiment of tweets matching the search term over the last 1, 5 and 15 minutes?

This is not intended to be a fully production ready application. We are not expecting any fancy gui - command line is fine, or the ability to change the search term after the application is started. Also we are not expecting you to create your own sentiment algorithm, there are plenty of open source libraries that are good enough for this proof of concept. You will need to set up a Twitter developer account if you don’t have one already.

# Installation
- Download the folder with the app
> git clone https://github.com/chessnocow/challenge
- Install requirements
>  pip install -r requirements.txt
- Install corpus for sentiment analysis
> python3 -m textblob.download_corpora
- Run the app (default query is "Kahoot")
> python3 main.py <search_query>

# Program interface

```
Updated 2022-10-11 17:55:56.847103
Metrics for query: Kahoot
Total number of tweets matching the query seen so far: 50
Tweets for last 1 minute: 1
Tweets for last 5 minutes: 3
Tweets for last 15 minutes: 7
Top tweeps for last 1  minute:
        bravehyacint with 1 tweets.
Top tweeps for last 5  minutes:
        petpetparkfan69 with 1 tweets.
        louvrephile with 1 tweets.
        bravehyacint with 1 tweets.
Top tweeps for last 15  minutes:
        bravehyacint with 2 tweets.
        krinhatriste_ with 1 tweets.
        Narutillo00 with 1 tweets.
        ozufy with 1 tweets.
        petpetparkfan69 with 1 tweets.
        louvrephile with 1 tweets.
The polarity of tweets for last 1  minute was neutral
The polarity of tweets for last 5  minutes was negative
The polarity of tweets for last 15  minutes was neutral
Press Ctrl+C to quit
```