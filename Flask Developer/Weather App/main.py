import requests
from datetime import time

url = 'http://api.weatherapi.com/v1/current.json'

with open('web/w_api_key.py', 'r') as f:
    api_key = f.read()


def if_city_exists(city):
    params = {'key': api_key, 'q': city, 'aqi': 'no'}
    resp_code = str(requests.get(url, params=params).status_code)
    if int(resp_code[0]) != 4:
        return True
    return False


def fetch_weather(city, city_id):
    params = {'key': api_key, 'q': city, 'aqi': 'no'}
    weather_data = requests.get(url, params=params).json()
    temperature = int(weather_data["current"]["temp_c"])
    weather_state = weather_data["current"]["condition"]["text"]
    current_time = weather_data["location"]["localtime"]

    return {'city': city, 'city_id': city_id,
            'degrees': temperature, 'state': weather_state,
            'skin': choose_time_skin(current_time)}


def choose_time_skin(curr_datetime: str):
    curr_time = curr_datetime.split(' ')[1]
    time_hours, time_minutes = [int(numb) for numb in curr_time.split(':')]
    current_time_formatted = time(time_hours, time_minutes)

    start_day = time(hour=10, minute=0)
    end_day = time(hour=18, minute=0)
    start_night = time(hour=22, minute=0)
    end_night = time(hour=6, minute=0)

    if start_day < current_time_formatted < end_day:
        return "card day"
    if current_time_formatted > start_night or current_time_formatted < end_night:
        return "card night"
    else:
        return "card evening-morning"