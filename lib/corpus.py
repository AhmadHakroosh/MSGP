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
        reddit.get_posts()

    def get_movies_data (self):
        print('gathering movies data')