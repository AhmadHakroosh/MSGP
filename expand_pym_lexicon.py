#!/usr/bin/python3

from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

'''
Expand the PYM Lexicon
'''

word_scores = {}

with open("pym_data.csv", "r") as pym_data_f:
    for line in pym_data_f:

        line = line.strip()

        (word, score) = line.split(",")
        word_scores[word.lower()] = float(score)


new_words = {}

for word in word_scores.keys():

    for syn in wn.synsets(word):

        #add definition
        definition_words = word_tokenize(syn.definition())

        for definition_word in definition_words:

            if (definition_word not in new_words.keys()):
                new_words[definition_word] = {"score": word_scores[word], "count": 1}

            else:

                new_words[definition_word]["count"] += 1
                new_words[definition_word]["score"] += (word_scores[word] - new_words[definition_word]["score"]) / new_words[definition_word]["count"]
           
        #add example words
        for example in syn.examples():

            example_words = word_tokenize(example)

            for example_word in example_words:

                if (example_word not in new_words.keys()):
                    new_words[example_word] = {"score": word_scores[word], "count": 1}

                else:

                    new_words[example_word]["count"] += 1
                    new_words[example_word]["score"] += (word_scores[word] - new_words[example_word]["score"]) / new_words[example_word]["count"]
 


        #add synonyms
        synonyms = syn.lemma_names()

        for synonym in synonyms:
            if (synonym not in new_words.keys()):
                new_words[synonym] = {"score": word_scores[word], "count": 1}

            else:

                new_words[synonym]["count"] += 1
                new_words[synonym]["score"] += (word_scores[word] - new_words[synonym]["score"]) / new_words[synonym]["count"]

        #add hyponyms
        hyponyms = syn.hyponyms()
        for hyponym_syn in hyponyms:
            for hyponym in hyponym_syn.lemma_names():

                if (hyponym not in new_words.keys()):
                    new_words[hyponym] = {"score": word_scores[word], "count": 1}

                else:

                    new_words[hyponym]["count"] += 1
                    new_words[hyponym]["score"] += (word_scores[word] - new_words[hyponym]["score"]) / new_words[hyponym]["count"]

        #add hypernyms
        hypernyms = syn.hypernyms()
        for hypernym_syn in hypernyms:
            for hypernym in hypernym_syn.lemma_names():

                if (hypernym not in new_words.keys()):
                    new_words[hypernym] = {"score": word_scores[word], "count": 1}

                else:

                    new_words[hypernym]["count"] += 1
                    new_words[hypernym]["score"] += (word_scores[word] - new_words[hypernym]["score"]) / new_words[hypernym]["count"]



for word in new_words.keys():
    print(word+","+str(new_words[word]["score"]))

#print(len(new_words))





