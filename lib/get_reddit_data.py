#!/usr/bin/python3

import json
import random
'''Load the Reddit corpus'''

class RedditData:

    def __init__(self):
        '''Load data from submissions.json'''
        self.data = []
        self.index = 0;

        js_data = None
        with open("submissions.json", "r") as submissions_f:
            js_data = json.load(submissions_f)

        for record in js_data:
            #only add labelled records
            if ("gender" in record.keys() and record["gender"] == "M" or  record["gender"] == "F"):
                if ("text" in record.keys()):
                    self.data.append((record["text"], record["gender"]))

        #shuffle data
        random.shuffle(self.data)


    def __iter__(self):
        return self

    def __next__(self):
        if (self.index < len(self.data)):
            
            sent = self.data[self.index]
            self.index += 1

            return sent

        else:
            raise StopIteration()





