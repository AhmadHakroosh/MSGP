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
            for post in self.API.subreddit(forum).new(params = REDDIT.last(REDDIT.limit)):
                post_object = Post(post)
                posts.append(post_object)
                print(len(posts))
                posts.extend(self.fetch_user_other_posts(post_object))
                print(len(posts))

        return posts

    def fetch_user_other_posts (self, post):
        posts = []
        if post.author.name is not 'N/A':
            for other_post in self.API.redditor(post.author.name).submissions.new(params = REDDIT.last(REDDIT.limit)):
                if other_post.id != post.id:
                    posts.append(Post(other_post, post.author))

        return posts



class Post:

    def __init__ (self, post, author = None):
        self.id = post.id

        if author is None:
            self.author = Author(post)
        else:
            self.author = author

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
            if any(gender in post.author_flair_text for gender in REDDIT.genders['m']):
                return 'm'
            elif any(gender in post.author_flair_text for gender in REDDIT.genders['f']):
                return 'f'
            else:
                return '?'
        else:
            return '?'