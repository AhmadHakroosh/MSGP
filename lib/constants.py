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
        self.period = 'year'
        self.genders = ['male', 'female']

    # API function
    def api (self, endpoint, keyword, after = None):
        url = {
            'subreddit': 'https://api.reddit.com/r/{}/new',
            'user': 'https://api.reddit.com/user/{}/submitted'
        }[endpoint].format(keyword)
        # Perform the AJAX and return found results
        response = requests.get(url, headers = self.headers, params = self.params(after)).json()['data']
        return [child['data'] for child in response['children']], response['after'], response['dist']

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

REDDIT = Reddit()