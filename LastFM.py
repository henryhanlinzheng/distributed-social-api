# lastfm.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

import urllib.request
import urllib.error
import json

class LastFM:
    def __init__(self) -> None:
        self._apikey = None
        self.top_tracks = None


    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        '''
        #TODO: assign apikey value to a class data attribute that can be accessed by class members
        self._apikey = apikey

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={self._apikey}&format=json&limit=1"
        #TODO: assign the necessary response data to the required class data attributes 

# e8d84a79cf0a5a5d6f86c969587ba6a5