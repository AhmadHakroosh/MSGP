#!/usr/bin/python3

'''Train and save a Word2Vec model using sentences from 
all_sents which is a pickle of all the sentences from the Reddit
and IMDB dataset
'''

import pickle

from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize


all_sentences = None

with open("all_sents", "rb") as all_sents_f:
    all_sentences = pickle.load(all_sents_f)

model = Word2Vec(size=100, window=5, min_count=1, workers=4)
model.build_vocab(all_sentences)
model.train(all_sentences, total_examples=model.corpus_count, epochs=1)
model.save("gender_word2vec.model")




