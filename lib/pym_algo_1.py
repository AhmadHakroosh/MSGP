#!/usr/bin/python3

from nltk.tokenize import word_tokenize

'''Calculate the PYM score of a test sentence
by averaging the PYM score of all known words in
the sentence
'''

class PYMScore:
    '''Compute the PYM score of a sentence'''
    def __init__(self):
        '''Initialize the scores from the data file pym_data.csv'''
        self.word_scores = {}

        with open("pym_data.csv", "r") as pym_data_f:

            for line in pym_data_f:

                line = line.strip()
                [word, score] = line.split(",")
                self.word_scores[word] = float(score)

    
    def get_pym_score(self, sentence):
        '''Calculate the PYM score of a sentence as the average
        score of all the (known) words in the sentence'''
        
        words = word_tokenize(sentence)

        mean_score = 0
        word_count = 0 

        for word in words:

            if (word.upper() in self.word_scores.keys()):

                word_score = self.word_scores[word.upper()]
                
                word_count += 1
                mean_score += (word_score - mean_score) / word_count

        return mean_score


    def pym_get_classification(self, score):
        '''A score of less than 0 is M, 0 is UNK and greater 
        than 0 is F'''

        if (score < 0):
            return "M"

        elif (score > 0):
            return "F"

        return "UNK"

