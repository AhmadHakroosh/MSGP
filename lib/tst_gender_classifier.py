#!/usr/bin/python3

import get_reddit_data
import get_imdb_data
import pickle

from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk

def get_features(sentence):

    words_vec = None
    words = word_tokenize(sentence)
    word_count = 0

    for word in words:

        try:
            vec = mod.get_vector(word)
            if (words_vec is None):
                words_vec = vec
            else:
                words_vec += vec

            word_count += 1
            
        except Exception:
            pass
    
    mean_words_vec = None

    features = {}

    if (words_vec is not None):

        mean_words_vec = words_vec / word_count

        words_vec_list = list(mean_words_vec)

        for index in range(0, len(words_vec_list)):
            features[str(index)] = words_vec_list[index]

    return features




reddit_data = get_reddit_data.RedditData()
imdb_data = get_imdb_data.IMDBData()

model = Word2Vec.load("gender_word2vec.model")
mod = model.wv

gender_classifier = None

with open("gender_classifier.model", "rb") as gender_classifier_f:
    gender_classifier = pickle.load(gender_classifier_f)


correct_label = 0

num_labels = 1000
cntr = 0

for x in imdb_data:
    
    gender = x[1]

    gender_features = get_features(x[0])
    classifier_gender = gender_classifier.classify(gender_features)

    if (gender == classifier_gender):
        correct_label += 1
       
    cntr += 1
    if (cntr >= num_labels):
        break

print("IMDB label accuracy: ", (correct_label/num_labels)*100)

correct_label = 0

#num_labels = 100
cntr = 0

for x in reddit_data:
    
    gender = x[1]
    #print("R: score of ", domains_score.get_domains_score(x[0]))

    gender_features = get_features(x[0])
    classifier_gender = gender_classifier.classify(gender_features)

    if (gender == classifier_gender):
        correct_label += 1
        
    cntr += 1
    if (cntr >= num_labels):
        break

print("Reddit label accuracy: ", (correct_label/num_labels)*100)


