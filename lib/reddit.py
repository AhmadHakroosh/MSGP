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
    def search (self, subreddit = None, author = None):
        # split into periods and iterate to find data and break limits of reddit
        for period in REDDIT.last('day', 1):
            # Initialize request parameters
            params = {
                'before': period['before'],
                'after': period['after'],
                'size': REDDIT.limit,
                'sort': 'desc'
            }
            # Set only if subreddit is given
            if subreddit is not None:
                params['subreddit'] = subreddit
            # Set only if author is given
            if author is not None:
                params['author'] = author
            # Execute the request
            response = requests.get(REDDIT.api, json = params)
            # Iterate over found results
            for result in response.json()['data']:
                # Instantiate a Post object
                post = Post(result)
                # Add the post for the class container of posts
                if post.id not in self.submissions:
                    self.submissions[post.id] = post
                    print(len(self.submissions))
                    # Check if the post is for a user that we've already looked for his posts
                    if post.author.name not in self.searched_authors:
                        # Search if not
                        self.searched_authors.append(author)
                        self.search(author = post.author.name)
        
        return self.submissions
    # Get posts from reddit
    def get_posts (self, store = None):
        # Iterate over a list of forums - see constants.py
        for forum in REDDIT.forums:
            print('Collecting posts from {}'.format(forum))
            # Search for posts under the given forum
            self.search(subreddit = forum)
        # Store data if asked to
        if store is not None:
            self.store_data(store, self.submissions)
        # Return found posts
        return self.submissions
    # Data storage function
    def store_data (self, location, data):
        # Create output location path if not exists
        os.makedirs(os.path.dirname(location), exist_ok = True)
        # Open the file location and write
        with open(location + '/submissions.tsv', 'w+') as store:
            for submission in data.values():
                entry = '{}\t{}\t{}'.format(submission['id'], submission['text'], submission['author'].gender)
                store.write(entry)
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