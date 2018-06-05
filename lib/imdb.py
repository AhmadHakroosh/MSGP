# Imports
from bs4 import BeautifulSoup
import os, requests, re, csv
import lib.constants as APP
# Retreive IMDB configuration - see constants.py
CONFIG = APP.IMDB

class IMDB:
    
    # Class instance initializer
    def __init__ (self):
        self.movies = []
        # self.movies = self.get_movie_titles(CONFIG.scripts_path)
        # self.get_imdb_movies_id()
        # self.get_movie_cast_list()
        self.get_character_genders()

    # Movie scripts scanner
    def get_movie_titles (self, path):
        movies = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                movies.append(re.sub(r'[\-]+', ' ',filename.replace('.txt', '')))
            break
        return movies
    
    # Movie ID getter throught IMDB
    def get_imdb_movies_id (self):
        movie_dictionary = {}
        for movie in self.movies:
            page = BeautifulSoup(requests.get(CONFIG.url, headers = {'Accept-Encoding': 'identity'}, params = {'q': movie}).text, 'html.parser')
            print(movie)
            if page.find('div', {'class': 'findSection'}) is not None:
                href = page.find('div', {'class': 'findSection'}).find('table').find('tr').find('td', {'class': 'result_text'}).find('a')['href']
                movie_id = href.split('/')[2]
                movie_dictionary[movie_id] = movie
        with open('{}/{}'.format(os.getcwd(), 'lib/data/movies/movie_titles.tsv'), 'w+') as document:
            for key in movie_dictionary:
                document.write('{}\t{}\n'.format(key, movie_dictionary[key]))
            document.close()

    # Movie cast list getter through IMDB
    def get_movie_cast_list (self):
        movies_cast_list = {}
        # Get all charcters details
        with open('{}/{}'.format(os.getcwd(), 'lib/data/movies/movie_titles.tsv'), 'r') as document:
            for entry in csv.reader(document, delimiter = '\t'):
                movie_id = entry[0]
                page = BeautifulSoup(requests.get(CONFIG.cast_url(movie_id) , headers = {'Accept-Encoding': 'identity'}).text, 'html.parser')
                cast_list = page.find('table', {'class': 'cast_list'})
                if cast_list is not None:
                    for actor in cast_list.findAll('tr', {'class': ['odd', 'even']}):
                        if actor.find('td', {'class': 'itemprop'}) is not None and actor.find('td', {'class': 'character'}) is not None:
                            actor_id = actor.find('td', {'class': 'itemprop'}).find('a')['href'].split('/')[2]
                            character = re.sub(r'[\s]+', ' ', actor.find('td', {'class': 'character'}).text.replace('\n', '').strip())
                            print('actor_id: {} | character: {}'.format(actor_id, character))
                            movies_cast_list['{}_{}'.format(movie_id, actor_id)] = {
                                'movie_id': movie_id,
                                'character': character
                            }
        # Write retrieved data
        with open('{}/{}'.format(os.getcwd(), 'lib/data/movies/movie_characters.tsv'), 'w+') as document:
            for character_id, character in movies_cast_list.items():
                document.write('{}\t{}\t{}\n'.format(character_id.split('_')[1], character['movie_id'], character['character']))
            document.close()

    # Get characters gender
    def get_character_genders (self):
        movies_cast_list = {}
        # Get all charcters details
        with open('{}/{}'.format(os.getcwd(), 'lib/data/movies/movie_characters.tsv'), 'r') as document:
            for entry in csv.reader(document, delimiter = '\t'):
                actor_id = entry[0]
                movie_id = entry[1]
                character = entry[2]
                page = BeautifulSoup(requests.get(CONFIG.actor_url(actor_id) , headers = {'Accept-Encoding': 'identity'}).text, 'html.parser')
                print('actor_id: {} | movie_id: {} | character: {}'.format(actor_id, movie_id, character))
                if page.find('div', {'id': 'name-job-categories'}) is not None:
                    jobs = page.find('div', {'id': 'name-job-categories'})
                    if jobs.find('a', {'href': '#actor'}) is not None:
                        job = jobs.find('a', {'href': '#actor'}).text.strip()
                        movies_cast_list['{}_{}'.format(movie_id, actor_id)] = {
                            'movie_id': movie_id,
                            'character': character,
                            'gender': CONFIG.jobs[job]
                        }
        # Write retrieved data
        with open('{}/{}'.format(os.getcwd(), 'lib/data/movies/movie_characters_gender.tsv'), 'w+') as document:
            for character_id, character in movies_cast_list.items():
                document.write('{}\t{}\t{}\t{}\n'.format(character_id.split('_')[1], character['movie_id'], character['character'], character['gender']))
            document.close()