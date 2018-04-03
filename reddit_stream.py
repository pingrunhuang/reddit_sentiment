import praw
from redis import ConnectionPool, Redis


            
class RedditBot():
    def __init__(self):
        self.reddit = praw.Reddit("bot2", user_agent="sentiment")

    def get_related_terms(self, keyword):
        pass

    def get_recent_reddit(self):
        subreddit = self.reddit.subreddit("all")
        for submission in subreddit.stream.submissions():
            print(submission.title)

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
    reddit_bot.get_recent_reddit()
