#!/usr/bin/python3

import pym_algo_2
import get_reddit_data
import get_imdb_data

reddit_data = get_reddit_data.RedditData()
imdb_data = get_imdb_data.IMDBData()

pym_score = pym_algo_2.PYM2Score()

correct_label = 0

num_labels = 1000
cntr = 0

for x in imdb_data:
    
    gender = x[1]

    #print("I: score of ", pym_score.get_pym_score(x[0]))
    pym_gender = pym_score.pym_get_classification(pym_score.get_pym_score(x[0]))
    #print("seen gender ", pym_gender)
    if (gender == pym_gender):
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
    #print("R: score of ", pym_score.get_pym_score(x[0]))

    pym_gender = pym_score.pym_get_classification(pym_score.get_pym_score(x[0]))

    if (gender == pym_gender):
        correct_label += 1
        
    cntr += 1
    if (cntr >= num_labels):
        break

print("Reddit label accuracy: ", (correct_label/num_labels)*100)



    



