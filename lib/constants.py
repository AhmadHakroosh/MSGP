import os, requests

# Reddit configuration
class Reddit:

    # Class instace initializer
    def __init__ (self):
        self.forums = [
            'AskMen',
            'AskWomen'
        ]
        self.total = 500
        self.limit = 100
        self.genders = ['male', 'female']

    # API function
    def api (self, endpoint, keyword, after = None):
        url = {
            'subreddit': 'https://api.reddit.com/r/{}/new',
            'user': 'https://api.reddit.com/user/{}/submitted'
        }[endpoint].format(keyword)
        # Perform the AJAX and return found results
        try:
            response = requests.get(url, headers = self.headers, params = self.params(after)).json()['data']
            return [child['data'] for child in response['children']], response['after'], response['dist']
        except:
            return [], '', 0

    # Params generator
    def params (self, after):
        obj = {
            'limit': REDDIT.limit,
            'author_flair_css_class': ','.join(self.genders)
        }
        if after is not None:
            obj['after'] = after
        return obj

    # Headers generator
    @property
    def headers (self):
        return {
            'user-agent': 'MSGP',
            'content-type': 'text'
        }

    # Store location property
    @property
    def store (self): 
        return os.getcwd() + '/lib/data/reddit/submissions.tsv'

# IMDB configuration
class Imdb:

    # Class instance initializer
    def __init__ (self):
        self.url = 'https://www.imdb.com/find'
        self.scripts_path = os.getcwd() + '/lib/data/movies/scripts'
        self.jobs = {
            'Actor': 'M',
            'Actress': 'F'
        }

    # Cast url getter
    def cast_url (self, movie_id):
        return 'https://www.imdb.com/title/{}/fullcredits'.format(movie_id)

    # Actor url getter
    def actor_url (self, actor_id):
        return 'https://www.imdb.com/name/{}/'.format(actor_id)

REDDIT = Reddit()
IMDB = Imdb()