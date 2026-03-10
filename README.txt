ICS 32 - Assignment 4: Extending the Platform

Author: Henry Hanlin Zheng
UCINetID: hhzheng1
Student ID: 19204536

This project is a continuation of the Distributed Social (DS) Journal App. 
It extends the platform's capabilities by introducing a transclusion feature 
that pulls live data from third-party web APIs and dynamically embeds it 
into user journal posts before they are saved locally or published to the 
DSP server.

1. OpenWeather API (@weather)
   - Retrieves the current temperature for a given zip code 
     (default: 92612, US) and replaces the "@weather" keyword in the post.

2. Last.FM API (@lastfm)
   - Retrieves the current #1 globally trending music track 
     and replaces the "@lastfm" keyword in the post.