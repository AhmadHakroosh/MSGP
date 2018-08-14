#!/usr/bin/python3

import json
import random

'''Get data from the IMDB Corpus'''

class IMDBData:
    def __init__(self):
        self.data = []
        self.index = 0;

        characters_js = None
        titles_js = None
        dialogues_js = None

        with open("movie_characters.json", "r") as characters_f:
            characters_js = json.load(characters_f)

        with open("movie_titles.json", "r") as titles_f:
            titles_js = json.load(titles_f)

        with open("movie_dialogues.json", "r") as dialogues_f:
            dialogues_js = json.load(dialogues_f)


        id_to_title = {}

        #set up id to title lookup table
        for movie in titles_js:
            if ( "movie_name" in movie.keys() and "movie_id" in movie.keys() ):

                movie_name = movie["movie_name"]
                movie_id = movie["movie_id"]

                id_to_title[movie_id] = movie_name

         #set up title to characters lookup table

        title_to_characters = {}

        for character in characters_js:
            if ("movie_id" in character.keys()):
                movie_id = character["movie_id"]

                if (movie_id in id_to_title.keys()):
                    movie_title = id_to_title[movie_id]

                     #get character

                    if ("character" in character.keys() and "gender" in character.keys() and (character["gender"] == "M" or character["gender"] == "F")):

                        character_name = character["character"]
                        character_gender = character["gender"]

                        if (not movie_title in title_to_characters):
                            title_to_characters[movie_title] = []
                             
                        title_to_characters[movie_title].append((character_name, character_gender))

                else:
                    print("No match for movie ", movie_id)



        #get dialogues

        for movie in dialogues_js:

            if ("movie" in movie.keys()):
                movie_title = movie["movie"]

                if (not movie_title in title_to_characters.keys()):

                    #look for matching substring
                    for cmp_movie_title in title_to_characters.keys():

                        cmp_movie_title_len = len(cmp_movie_title)

                        if (movie_title[0:cmp_movie_title_len] == cmp_movie_title):
                            movie_title = cmp_movie_title
                            break


                if (movie_title in title_to_characters.keys()):

                    if ("script" in movie.keys()):
                        
                        for script in movie["script"]:

                            if ( "character" in script.keys() and "dialog" in script.keys() ):

                                character = script["character"]
                                seen_character = False
                                

                                for ( character_name, character_gender ) in title_to_characters[movie_title]:

                                    if (character_name.upper() == character.upper()):

                                        for line in script["dialog"]:
                                                self.data.append((line, character_gender))


    def __iter__(self):
        return self

    def __next__(self):
        if (self.index < len(self.data)):
            
            sent = self.data[self.index]
            self.index += 1

            return sent

        else:
            raise StopIteration()




