import time
# Constants
NOW = int(time.time())
DAY = 60 * 60 * 24
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY
# Reddit configuration
class Reddit:
    def __init__ (self):
        self.api = 'https://api.pushshift.io/reddit/submission/search?'
        self.forums = [
            'AskMen',
            'AskWomen'
        ]
        self.limit = '100000'
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
    # Accepts a period to find posts through, returns a list of period blocks
    def last (self, total = 'year', x = 1, periods = 'month'):
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