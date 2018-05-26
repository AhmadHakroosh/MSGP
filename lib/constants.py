import time

NOW = time.time()
DAY = 60 * 60 * 24
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY

class REDDIT:
    client_id = 'xZli_mehJLtd7w'
    client_secret = 'zvMUu0_Wc09t97h4k2zLglP24sU'
    username = 'AhmadHakroosh'
    password = '1A$h50187'
    user_agent = 'MSGP'
    forums = [
        'AskMen',
        'AskWomen'
    ]
    limit = 'year'
    genders = {
        'm': [
            'Male',
            '♂'
        ],
        'f': [
            'Female',
            '♀'
        ]
    }
    def last (self, t, x = 1):
        return 'timestamp:{}..{}'.format(NOW, {
            'day': NOW - (x * DAY),
            'week': NOW - (x * (7 * DAY)),
            'month': NOW - (x * (30 * DAY)),
            'year': NOW - (x * (365 * DAY))
        }[t])