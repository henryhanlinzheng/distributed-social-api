# a4.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

from OpenWeather import OpenWeather
from LastFM import LastFM
import ui

def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)


open_weather = OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
lastfm = LastFM()

test_api("Testing the weather: @weather", "8d3ac5e3ca6195edc3ab385fffeef6a2", open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm", "e8d84a79cf0a5a5d6f86c969587ba6a5", lastfm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword


if __name__ == '__main__':
    ui.run()