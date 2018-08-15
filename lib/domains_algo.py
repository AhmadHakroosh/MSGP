#!/usr/bin/python3

from nltk.tokenize import word_tokenize

'''Estimate the most probable domain of a sentence
by looking for a set of keywords
'''

class DomainScore:
    '''Compute the PYM score of a sentence'''
    def __init__(self):
        '''Initialize the scores from the data file domain_data.csv'''
        self.word_scores = {}

        with open("domain_data.csv", "r") as domain_data_f:

            for line in domain_data_f:
                line = line.strip()
                [word, score] = line.split(",")
                self.word_scores[word] = float(score)

    
    def get_domain_score(self, sentence):
        '''Determine the domain score of a sentence by averaging the
        score of all the (known) words in the sentence'''
        
        words = word_tokenize(sentence)

        mean_score = 0
        word_count = 0 

        for word in words:

            if (word.lower() in self.word_scores.keys()):

                word_score = self.word_scores[word.lower()]
                
                word_count += 1
                mean_score += (word_score - mean_score) / word_count

        return mean_score


    def domain_get_classification(self, score):
        '''A score of less than 0 is M, 0 is UNK and greater 
        than 0 is F'''

        if (score < 0):
            return "M"

        elif (score > 0):
            return "F"

        return "UNK"

