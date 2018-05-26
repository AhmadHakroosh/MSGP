import praw
import lib.constants as APP

REDDIT = APP.REDDIT()

class Reddit_API:
    
    def __init__ (self):
        self.API = praw.Reddit(
            client_id = REDDIT.client_id,
            client_secret = REDDIT.client_secret,
            username = REDDIT.username,
            password = REDDIT.password,
            user_agent = REDDIT.user_agent
        )

    def get_posts (self):
        posts = []

        for forum in REDDIT.forums:
            for post in self.API.subreddit(forum).hot(limit = REDDIT.limit):
                posts.append(Post(post))

        return posts


class Post:

    def __init__ (self, post):
        self.author = Author(post)
        self.text = self.get_text(post)

    def get_text (self, post):
        if not post.selftext and len(post.selftext.split(' ')) > 5:
            return post.selftext
        else:
            return post.title


class Author:

    def __init__ (self, post):
        if post.author is not None:
            self.name = post.author.name
        else:
            self.name = 'N/A'

        self.gender = self.get_gender(post)

    def get_gender (self, post):
        if post.author_flair_text is not None:
            if any(gender in post.author_flair_text for gender in APP.GENDERS['m']):
                return 'm'
            elif any(gender in post.author_flair_text for gender in APP.GENDERS['f']):
                return 'f'
            else:
                return '?'
        else:
            return '?'