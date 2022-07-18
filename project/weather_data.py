import json

import geocoder
import requests

from api_secrets import OPEN_WEATHER_API_KEY


def get_weather():
    # Retrieve tuple of latitude and longitute coords from ip
    g = geocoder.ip('me')
    lat, lon = g.latlng

    # Initialize Service URL
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}&units=imperial"

    # Retrieve response
    response = requests.get(url)

    # Check for errors in GET request
    if response.status_code != 200:
        return "I'm unable to gather weather data on your location"
    
    # Convert reponse to dict
    data = json.loads(response.text)

    # Collect data from API response
    loc = data['name']
    temp = round(data['main']['temp'])
    desc = data['weather'][0]['description']
    high = round(data['main']['temp_max'])
    low = round(data['main']['temp_min'])
    
    # Return formatted string to bot as response
    return f'In {loc} it is currently {temp} degrees Fahrenheit. Today, you can expect {desc} with a high of {high} degrees and a low of {low} degrees'
