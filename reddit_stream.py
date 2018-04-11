# -*- coding:utf-8 -*-
import praw
from redis import ConnectionPool, Redis
from model import Sentiment
from sqlalchemy import create_engine
# from DBUtil import database
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class RedditBot():
    def __init__(self):
        self.reddit = praw.Reddit("bot1", user_agent="sentiment")

    def get_related_terms(self, keyword):
        pass

    def store_recent_reddit(self, sentiment_term="all"):
        # maximum number of reddits to store in mem, probably use redis for caching
        MAX_REDDIT_TO_COMMIT = 10
        # generate the sentiment table for storing sentiment data
        def get_sentiment(text):
            analyzer = SentimentIntensityAnalyzer()
            """
            Return a float for sentiment strength based on the input text.
            Positive values are positive valence, negative value are negative
            valence.
            """
            vs = analyzer.polarity_scores(text)
            return str(vs["compound"])
        database.gen_sentiment_table()

        subreddit = self.reddit.subreddit(sentiment_term)
        recent_reddits = []
        for submission in subreddit.stream.submissions():
            new_reddit = Sentiment()
            new_reddit.title = str(submission.title)
            new_reddit.unix = str(submission.created_utc)
            new_reddit.sentiment = get_sentiment(submission.title)
            new_reddit.category = sentiment_term
            recent_reddits.append(new_reddit)
            print(submission.title)

            if len(recent_reddits)==MAX_REDDIT_TO_COMMIT:
                database.insert("sentiment", recent_reddits)
                recent_reddits=[]

    def get_positive_negative_percentage(self, keyword):
        pass

    def auto_reply(self, topic):
        '''
        This method reply the basic questions such as "who is", "what is", "what is" .etc with google answer powered by LMGTFY
        '''
        from urllib.parse import quote_plus
        QUESTIONS = ["who is", "what is", "what is"]
        REPLY_TEMPLATE = "[Let me google it for you](http://lmgtfy.com/?q={})"
        subreddit = self.reddit.subreddit(topic)
        for submission in subreddit.stream.submissions():
            if len(submission.title.split())>10:
                pass
            title = submission.title.lower()
            for question_phrase in QUESTIONS:
                if question_phrase in title:
                    url_title = quote_plus(title)
                    reply_content = REPLY_TEMPLATE.format(url_title)
                    print("Reply to ", title)
                    submission.reply(reply_content)
                    break

if __name__=="__main__":
    reddit_bot = RedditBot()
    reddit_bot.store_recent_reddit(sentiment_term="china")
