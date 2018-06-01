# Imports
from bs4 import BeautifulSoup
import os, requests
import lib.constants as APP
# Retreive IMDB configuration - see constants.py
CONFIG = APP.IMDB

class IMDB:
    
    # Class instance initializer
    def __init__ (self):
        