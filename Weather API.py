# Homework 02

## Open Weather API

## Goal

To illustrate how to use an API to collect weather-related data. 

## Instructions 

In this assignment you are asked to register a free account on [https://openweathermap.org/](https://openweathermap.org/).
Then study the API's documentation to extract weather info from locations described in data/locations.csv.
Your program should save the collected info in JSON format, similar to: 

```
[
    {"today": "2021-09-01 14:41:32", "city": "Denver", "state": "CO", "temp_min": 80, "temp_max": 91, "temp": 86}, 
    {"today": "2021-09-01 14:41:32", "city": "Colorado Springs", "state": "CO", "temp_min": 70, "temp_max": 89, "temp": 82}, 
    {"today": "2021-09-01 14:41:32", "city": "Aspen", "state": "CO", "temp_min": 54, "temp_max": 73, "temp": 64}, 
    {"today": "2021-09-01 14:41:32", "city": "Phoenix", "state": "AR", "temp_min": 86, "temp_max": 94, "temp": 90}, 
    {"today": "2021-09-01 14:41:32", "city": "Tucson", "state": "AR", "temp_min": 80, "temp_max": 89, "temp": 85},
    {"today": "2021-09-01 14:41:32", "city": "Los Angeles", "state": "CA", "temp_min": 67, "temp_max": 85, "temp": 73}, 
    {"today": "2021-09-01 14:41:32", "city": "Bethlehem", "state": "PA", "temp_min": 64, "temp_max": 72, "temp": 66}, 
    {"today": "2021-09-01 14:41:32", "city": "Miami", "state": "FL", "temp_min": 86, "temp_max": 96, "temp": 91}, 
    {"today": "2021-09-01 14:41:32", "city": "Boston", "state": "MA", "temp_min": 64, "temp_max": 69, "temp": 66}
]
```


import requests
import json
import os
from urllib.parse import urlencode
from datetime import datetime
import time
import math

# definitions/parameters
DATA_FOLDER = os.path.join('..', 'data')
LOCATIONS_FILE_NAME = 'locations.csv'
JSON_FILE_NAME = 'weather.json'
OPEN_WEATHER_API = 'http://api.openweathermap.org/data/2.5/weather'
SLEEP_TIME = 5


def kelvin_fahrenheit(k):
    return math.floor((k - 273.15) * 9 / 5 + 32)


def make_request(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=ef729dcbe94491bf50a431e7a21636b3"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOCATIONS_FILE_NAME, "r") as file:
        text = file.read().strip()
        lines = text.split("\n")

        result =[]

        for line in lines:
            parts = line.split(",")
            city = parts[0]
            state = parts[1]

            data = make_request(city)

            temp= kelvin_fahrenheit(data["main"]["temp"])
            temp_min= kelvin_fahrenheit(data["main"]["temp_min"])
            temp_max= kelvin_fahrenheit(data["main"]["temp_max"])

            row = {
                "today": today,
                "city": city,
                "state": state,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "temp": temp
            }
            result.append(row)
    with open(JSON_FILE_NAME, "w") as file:
        json.dump(result, file, indent=4)

