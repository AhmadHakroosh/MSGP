import os, time, praw
# Constants
NOW = int(time.time())
DAY = 60 * 60 * 24
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY
# Reddit configuration
class Reddit:
    def __init__ (self):
        self.api = praw.Reddit(
            client_id='xZli_mehJLtd7w',
            client_secret='zvMUu0_Wc09t97h4k2zLglP24sU',
            username='AhmadHakroosh',
            password='1A$h50187',
            user_agent='MSGP'
        )
        self.forums = [
            'AskMen',
            'AskWomen'
        ]
        self.limit = '1'
        self.period = 'year'
        self.genders = {
            'm': [
                'male',
                'Male',
                '♂'
            ],
            'f': [
                'female',
                'Female',
                '♀'
            ]
        }
    # Store location property
    @property
    def store (self): 
        return os.getcwd() + '/lib/data/reddit/submissions.tsv'
    # Accepts a period to find posts through, returns a list of period blocks
    def last (self, total = 'year', x = 1, periods = 'week'):
        times = {
            'day': DAY,
            'week': WEEK,
            'month': MONTH,
            'year': YEAR
        }
        if times[total] * x <= times[periods]:
            return [{
                'before': str(NOW),
                'after': str(NOW - (times[total] * x))
            }]
        else:
            all_periods = []
            for period in range(int((times[total] * x) / times[periods])):
                all_periods.append({
                    'before': str(NOW - (period * times[periods])),
                    'after': str(NOW - ((period + 1) * times[periods]))
                })
            return all_periods

REDDIT = Reddit()