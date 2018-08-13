#!/usr/bin/python3

'''
Convert Gend scores 
from the PYM dataset to values between -1(most masculine)
and +1 (most feminine)
'''

import re

num_re = re.compile("^\d+(\.\d+)?$")

with open("pym_data.txt", "r") as pym_data_f:
    for line in pym_data_f:

        line = line.strip()
        parameters = line.split()

        #valid data
        if (len(parameters) == 35):

            word = parameters[2]
            gend  = parameters[32]

            if (re.match(num_re, gend)):

                new_score = (float(gend) - 4.05)/4.05;
                print(word + "," + str(new_score))
        
