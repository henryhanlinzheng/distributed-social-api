# openweather.py

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

class OpenWeather(WebAPI):
    def __init__(self, zipcode="92612", ccode="US") -> None:
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        self._apikey = None
        self.temperature = None
        self.high_temp = None
        self.low_temp = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset=None

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self._apikey}"
        #TODO: assign the necessary response data to the required class data attributes 
        data = self._download_url(url)

        self.temperature = data['main']['temp']
        self.high_temp = data['main']['temp_max']
        self.low_temp = data['main']['temp_min']
        self.longitude = data['coord']['lon']
        self.latitude = data['coord']['lat']
        self.description = data['weather'][0]['description']
        self.humidity = data['main']['humidity']
        self.city = data['name']
        self.sunset = data['sys']['sunset']
        
    def transclude(self, message:str) -> str:
        '''
        Replaces @openweather keyword with the current temperature in the city specified by the zipcode and ccode.
        :param message: Message to transclude
        :returns: Transcluded message
        '''
        if "@weather" in message and self.temperature is not None:
            return message.replace("@weather", str(self.temperature))
        return message
