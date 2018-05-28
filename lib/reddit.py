import lib.constants as APP
import requests

REDDIT = APP.REDDIT

class Reddit:

    def search (self, params):
        response = requests.get(REDDIT.api, json = params)
        return response.json()['data']

    def get_posts (self):
        posts = []
        for forum in REDDIT.forums:
            print('Collecting posts from {}'.format(forum))
            for period in REDDIT.last('month', 3):
                params = {
                    'subreddit': forum,
                    'before': period['before'],
                    'after': period['after'],
                    'size': REDDIT.limit,
                    'sort': 'desc'
                }
                for post in self.search(params):
                    post_object = Post(post)
                    posts.append(post_object)
                    posts.extend(self.fetch_user_other_posts(post_object))

        return posts

    def fetch_user_other_posts (self, post):
        posts = []
        if post.author.name is not 'N/A':
            for period in REDDIT.last('month', 3):
                params = {
                    'author': post.author.name,
                    'before': period['before'],
                    'after': period['after'],
                    'size': REDDIT.limit,
                    'sort': 'desc'
                }
                for other_post in self.search(params):
                    if other_post['id'] != post.id:
                        posts.append(Post(other_post, post.author))

        return posts



class Post:

    def __init__ (self, post, author = None):
        self.id = post['id']

        if author is None:
            self.author = Author(post)
        else:
            self.author = author

        self.text = self.get_text(post)

    def get_text (self, post):
        if not not post['selftext'] and len(post['selftext'].split(' ')) > 5:
            return post['selftext']
        else:
            return post['title']


class Author:

    def __init__ (self, post):
        if post['author'] is not None:
            self.name = post['author']
        else:
            self.name = 'N/A'

        self.gender = self.get_gender(post)

    def get_gender (self, post):
        if post['author_flair_text'] is not None:
            if any(gender in post['author_flair_text'] for gender in REDDIT.genders['m']):
                return 'm'
            elif any(gender in post['author_flair_text'] for gender in REDDIT.genders['f']):
                return 'f'
            else:
                return '?'
        else:
            return '?'