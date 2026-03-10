# openweather.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

class OpenWeather:
    def __init__(self, zipcode="92612", ccode="US") -> None:
        self.zipcode = zipcode
        self.ccode = ccode
        self._apikey = None
        self.temperature = None
        self.high_temp = None
        self.low_temp = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset=None


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
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self._apikey}"
        #TODO: assign the necessary response data to the required class data attributes
        pass
        
    
