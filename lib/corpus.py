from lib.reddit import Reddit
import lib.constants as APP

reddit = Reddit()

class Corpus:

    def __init__ (self):
        self.get_data()
    
    def get_data (self):
        print('loading data...')
        self.get_reddit_data()
        self.get_movies_data()

    def get_reddit_data (self):
        print('gathering reddit data')
        print(len(reddit.get_posts()))

    def get_movies_data (self):
        print('gathering movies data')