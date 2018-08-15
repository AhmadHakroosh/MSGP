#!/usr/bin/python3

from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from itertools import chain
import re


'''Find word domains keywords'''

domains = {

        "clothing":  1,
        "color":  1,
        "home":  1,
        "food":  1,
        "drink":  1,
        "body":  1,
        "health":  1,
        "relationship":  1,
        "time":  1,

        "swear":  -1,
        "car":  -1,
        "traffic":  -1,
        "work":  -1,
        "computing":  -1,
        "sport":  -1,
        "politics":  -1

        }

domain_words = {}
stop_words = stopwords.words("english")

for domain in domains:


    domain_score = domains[domain]
    domain_words[domain] = {"score": domain_score, "count": 1}

    for syn in wn.synsets(domain):

        synonyms = syn.lemma_names()

        for synonym in synonyms:
           
            if (synonym not in domain_words.keys()):
                domain_words[synonym] = {"score": domain_score, "count": 1}

            else:

                domain_words[synonym]["count"] += 1
                domain_words[synonym]["score"] += (domain_score - domain_words[synonym]["score"]) / domain_words[synonym]["count"]

#'''        
        #add definition
        definition_words = word_tokenize(syn.definition())

        for definition_word in definition_words:
            #if (definition_word in stop_words):
            #    continue

            if (definition_word not in domain_words.keys()):
                domain_words[definition_word] = {"score": domain_score, "count": 1}

            else:

                domain_words[definition_word]["count"] += 1
                domain_words[definition_word]["score"] += (domain_score - domain_words[definition_word]["score"]) / domain_words[definition_word]["count"]
           
        #add example words
        for example in syn.examples():

            example_words = word_tokenize(example)

            for example_word in example_words:
                #if (example_word in stop_words):
                #    continue

                if (example_word not in domain_words.keys()):
                    domain_words[example_word] = {"score": domain_score, "count": 1}

                else:

                    domain_words[example_word]["count"] += 1
                    domain_words[example_word]["score"] += (domain_score - domain_words[example_word]["score"]) / domain_words[example_word]["count"]
 
#'''

#'''
        #add hyponyms
        hyponyms = syn.hyponyms()
        for hyponym_syn in hyponyms:

            definition_words = word_tokenize(hyponym_syn.definition())    

            for hyponym in chain(definition_words, hyponym_syn.lemma_names()):

                if (hyponym not in domain_words.keys()):
                    domain_words[hyponym] = {"score": domain_score, "count": 1}

                else:

                    domain_words[hyponym]["count"] += 1
                    domain_words[hyponym]["score"] += (domain_score - domain_words[hyponym]["score"]) / domain_words[hyponym]["count"]

        #add hypernyms
        hypernyms = syn.hypernyms()
        for hypernym_syn in hypernyms:

            definition_words = word_tokenize(hypernym_syn.definition())    

            for hypernym in chain(definition_words, hypernym_syn.lemma_names()):

                if (hypernym not in domain_words.keys()):
                    domain_words[hypernym] = {"score": domain_score, "count": 1}

                else:

                    domain_words[hypernym]["count"] += 1
                    domain_words[hypernym]["score"] += (domain_score - domain_words[hypernym]["score"]) / domain_words[hypernym]["count"]



plain_words_re = re.compile("^[a-z\-]+$")

for word in domain_words.keys():
    score = domain_words[word]["score"]
    if ((score < 0 and score >= -1) or (score > 0 and score <= 1) ): 
        if (re.match(plain_words_re, word)):
            print(word+","+str(domain_words[word]["score"]))


