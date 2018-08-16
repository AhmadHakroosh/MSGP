
import get_reddit_data
import get_imdb_data
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import pickle

'''Train Model on the mean of its Word2Vec Vector
'''

reddit_data = get_reddit_data.RedditData()
imdb_data = get_imdb_data.IMDBData()

model = Word2Vec.load("gender_word2vec.model")
mod = model.wv

train_data_set = []

training_size = 2000
cntr = 0

for x in imdb_data:

    sentence = x[0]   
    gender = x[1]

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

    if (words_vec is not None):

        features = {}

        mean_words_vec = words_vec / word_count

        words_vec_list = list(mean_words_vec)

        for index in range(0, len(words_vec_list)):
            features[str(index)] = words_vec_list[index]

        train_data_set.append((features, gender))


    cntr = cntr+1
    if (cntr > training_size):
        break

cntr = 0
for x in reddit_data:

    sentence = x[0]   
    gender = x[1]

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

    if (words_vec is not None):

        features = {}

        mean_words_vec = words_vec / word_count

        words_vec_list = list(mean_words_vec)

        for index in range(0, len(words_vec_list)):
            features[str(index)] = words_vec_list[index]

        train_data_set.append((features, gender))


    cntr = cntr+1
    if (cntr > training_size):
        break


gender_classifier = nltk.NaiveBayesClassifier.train(train_data_set)

with open("gender_classifier.model", "wb") as gender_classifier_f:
    pickle.dump(gender_classifier, gender_classifier_f)


