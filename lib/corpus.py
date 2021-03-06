from lib.reddit import Reddit
from lib.imdb import IMDB
import lib.constants as APP

reddit = Reddit()
imdb = IMDB()

class Corpus:

    def __init__ (self):
        self.get_data()
    
    def get_data (self):
        print('Loading data')
        # self.get_reddit_data()
        self.get_movies_data()

    def get_reddit_data (self):
        print('Gathering reddit data')
        print('Collected {} posts from reddit.'.format(len(reddit.get_posts())))

    def get_movies_data (self):
        print('Gathering movies data')