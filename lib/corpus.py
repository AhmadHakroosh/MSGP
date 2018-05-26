from lib.reddit import Reddit_API
import lib.constants as APP

reddit = Reddit_API()
REDDIT = APP.REDDIT()

class Corpus:

    def __init__ (self):
        self.get_data()
    
    def get_data (self):
        print('loading data...')
        self.get_reddit_data()

    def get_reddit_data (self):
        print('gathering data from reddit')
        reddit.get_posts()

        print('hello')


        # for forum_name in CONSTANTS.REDDIT['forums']:
        #     forum = reddit.subreddit(forum_name)
        #     for post in forum.hot():
        #         if post.author_flair_text != None and any(gender in post.author_flair_text for gender in ['Male', 'Female', '♂', '♀']):
        #             if not post.selftext and len(post.selftext.split(' ')) > 5:
        #                 print(post.selftext)
        #             else:
        #                 print(post.title)
        #             print(post.author_flair_text)

    def get_movies_data (self):
        print('gathering movies data')



