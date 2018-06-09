# Imports
import lib.constants as APP
import os, requests
# Retreive Reddit configuration - see constants.py
REDDIT = APP.REDDIT
authors = []

# Reddit class definition
class Reddit:
    # Class initializer
    def __init__ (self):
        self.submissions = {}

    # Search function that accepts a subreddit, an author name, both, or nothing
    def search (self, subreddit = None, author = None, after = None, count = 100):
        # Find subreddit posts
        if subreddit is not None:
            # Split into steps of 100 from 0 to pre-define number of posts and search
            for _ in range(0, REDDIT.total, REDDIT.limit):
                # Execute the request
                results, after, _ = REDDIT.api('subreddit', subreddit, after)
                # Iterate over found results
                for result in results:
                    # Instantiate a Post object
                    post = Post(result)
                    # Add the post for the class container of posts
                    if post.id not in self.submissions:
                        self.submissions[post.id] = post
        # Find user posts
        if author is not None:
            while count == 100:
                # Execute the request
                results, after, count = REDDIT.api('user', author.name, after)
                # Iterate over found results
                for result in results:
                    # Instantiate a Post object
                    post = Post(result, author)
                    # Add the post for the class container of posts
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
        # Search each author posts
        for author in authors:
            print('Collecting posts of {}'.format(author.name))
            self.search(author = author)
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
            authors.append(self.author)
        else:
            self.author = author

        self.text = self.get_text(post)

    # Text fetch
    def get_text (self, post):
        if post['selftext'] != '' and len(post['selftext'].split(' ')) > 5:
            return post['selftext']
        else:
            return post['title']

    # Class object representation
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
        if post['author_flair_css_class'] is not None:
            if any(gender in post['author_flair_css_class'] for gender in REDDIT.genders):
                return post['author_flair_css_class'][0]
            else:
                return '?'
        else:
            return '?'