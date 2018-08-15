#!/usr/bin/python3

import domains_algo
import get_reddit_data
import get_imdb_data

reddit_data = get_reddit_data.RedditData()
imdb_data = get_imdb_data.IMDBData()

domains_score = domains_algo.DomainScore()

correct_label = 0

num_labels = 1000
cntr = 0

for x in imdb_data:
    
    gender = x[1]

    #print("I: score of ", domains_score.get_domains_score(x[0]))
    domains_gender = domains_score.domain_get_classification(domains_score.get_domain_score(x[0]))
    #print("seen gender ", domains_gender)
    if (gender == domains_gender):
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

    domains_gender = domains_score.domain_get_classification(domains_score.get_domain_score(x[0]))

    if (gender == domains_gender):
        correct_label += 1
        
    cntr += 1
    if (cntr >= num_labels):
        break

print("Reddit label accuracy: ", (correct_label/num_labels)*100)



    



