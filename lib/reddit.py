import praw
from constants import __CONSTANTS__

CONSTANTS = __CONSTANTS__()

REDDIT = CONSTANTS.REDDIT

class Reddit_API:
    def __init__ (self):
        self = praw.Reddit(
            client_id = REDDIT['client_id'],
            client_secret = REDDIT['client_secret'],
            username = REDDIT['username'],
            password = REDDIT['password'],
            user_agent = REDDIT['user_agent']
        )