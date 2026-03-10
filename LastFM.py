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
from WebAPI import WebAPI

class LastFM(WebAPI):
    def __init__(self) -> None:
        super().__init__()
        self.top_tracks = None

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={self.apikey}&format=json&limit=1"
        #TODO: assign the necessary response data to the required class data attributes 
        response = urllib.request.urlopen(url)
        json_results = response.read()
        data = json.loads(json_results)

        self.top_tracks = data['tracks']['track'][0]['name']
        
        if response in locals() and response is not None:
            response.close()

    def transclude(self, message:str) -> str:
        '''
        Replaces @lastfm keyword with the top trending track.
        :param message: Message to transclude
        :returns: Transcluded message
        '''
        if self.top_tracks is not None:
            return message.replace("@lastfm", self.top_tracks)
        return message