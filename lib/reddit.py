import lib.constants as APP
import requests

REDDIT = APP.REDDIT

class Reddit:

    def __init__ (self):
        self.submissions = []
        self.searched_authors = []

    def search (self, subreddit = None, author = None):
        for period in REDDIT.last('year', 1):
            params = {
                'before': period['before'],
                'after': period['after'],
                'size': REDDIT.limit,
                'sort': 'desc'
            }

            if subreddit is not None:
                params['subreddit'] = subreddit
            if author is not None:
                params['author'] = author
            
            response = requests.get(REDDIT.api, json = params)
            for result in response.json()['data']:
                post = Post(result)
                self.submissions.append(post)
                if post.author.name not in self.searched_authors:
                    self.searched_authors.append(author)
                    self.search(author = post.author.name)
        
        return self.submissions

    def get_posts (self):
        for forum in REDDIT.forums:
            print('Collecting posts from {}'.format(forum))
            self.search(subreddit = forum)

        return self.submissions


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