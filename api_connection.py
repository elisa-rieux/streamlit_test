""" This script store the function required to stream data from the API of your choice"""

import requests
import json
import pandas as pd
import numpy as np

# create GET request

def get_data_from_api(city):
    
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': '296f04ea9e6e74b65b53c900c732b2e8',
        'units': 'metric'
    }

    response = requests.get(url, params=params)
    outputs = response.json()

    return outputs

def get_data_forecast(city):
    url = 'http://api.openweathermap.org/data/2.5/forecast'  # Modification ici
    params = {
        'q': city,
        'appid': '296f04ea9e6e74b65b53c900c732b2e8',
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    outputs = response.json()
    return outputs
