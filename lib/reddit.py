# Imports
import lib.constants as APP
import os, requests
# Retreive Reddit configuration - see constants.py
REDDIT = APP.REDDIT

# Reddit class definition
class Reddit:
    # Class initializer
    def __init__ (self):
        self.submissions = {}
        self.searched_authors = []
    # Search function that accepts a subreddit, an author name, both, or nothing
    def search (self, subreddit):
        # split into periods and iterate to find data and break limits of reddit
        for period in REDDIT.last('month', 1):
            # Initialize request parameters
            params = {
                'before': period['before'],
                'after': period['after'],
                'size': REDDIT.limit,
                'sort': 'desc'
            }
            # Set subreddit
            params['subreddit'] = subreddit
            # Execute the request
            subreddit_results = REDDIT.api.subreddit()
            # Iterate over found results
            for result in subreddit_results.json()['data']:
                # Instantiate a Post object
                post = Post(result)
                # Add the post for the class container of posts
                if post.id not in self.submissions:
                    self.submissions[post.id] = post
                    # Check if the post is for a user that we've already looked for his posts
                    if post.author.name not in self.searched_authors:
                        # Search if not
                        params.pop('subreddit', None)
                        params['author'] = post.author.name
                        user_results = requests.get(REDDIT.api, json = params)
                        for result in user_results.json()['data']:
                            # Instantiate a Post object
                            post = Post(result)
                            if post.id not in self.submissions:
                                self.submissions[post.id] = post
        
        return self.submissions
    # Get posts from reddit
    def get_posts (self, save = True):
        # Iterate over a list of forums - see constants.py
        for forum in REDDIT.forums:
            print('Collecting posts from {}'.format(forum))
            # Search for posts under the given forum
            self.search(subreddit = forum)
        # Store data if asked to
        if save:
            self.store_data(self.submissions)
        # Return found posts
        return self.submissions
    # Data storage function
    def store_data (self, data):
        # Create output location path if not exists
        os.makedirs(os.path.dirname(REDDIT.store), exist_ok = True)
        # Open the file location and write
        with open(REDDIT.store, 'w+') as store:
            for submission in data.values():
                store.write('{}\n'.format(str(submission)))
            # Close the store
            store.close()

# Post class
class Post:
    # Class initializer
    def __init__ (self, post, author = None):
        self.id = post['id']

        if author is None:
            self.author = Author(post)
        else:
            self.author = author

        self.text = self.get_text(post)
    # Text fetch
    def get_text (self, post):
        if not not post['selftext'] and len(post['selftext'].split(' ')) > 5:
            return post['selftext']
        else:
            return post['title']

    def __repr__ (self):
        return '{}\t{}\t{}'.format(self.id, self.text.replace("\r","").replace("\n","") , self.author.gender)

# Author class
class Author:
    # Class initializer
    def __init__ (self, post):
        if post['author'] is not None:
            self.name = post['author']
        else:
            self.name = 'N/A'

        self.gender = self.get_gender(post)
    # Gender finder
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