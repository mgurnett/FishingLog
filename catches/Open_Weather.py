import requests
from zoneinfo import ZoneInfo
from datetime import datetime
from django.conf import settings
    
localtz = ZoneInfo('America/Edmonton')
utc = ZoneInfo('UTC')
OW_API_KEY = settings.OW_API_KEY

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

def make_url (lat, lon):
    return f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={OW_API_KEY}'

def get_data (lake):
    # print (make_url (float(round(lake.lat,4)), float(round(lake.long,4))) )
    return requests.get( make_url (float(round(lake.lat,4)), float(round(lake.long,4))) )

def time_convert (time, offset):
    return datetime.fromtimestamp( time + offset )

def current (response):
    current = {}

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']

        current['timezone'] =           data['timezone']
        current['time_taken'] =         time_convert ( data['current']['dt'], timezone_offset ).strftime("%-I:%M %p")
        current['sunrise'] =            time_convert ( data['current']['sunrise'], timezone_offset ).strftime("%-I:%M %p")
        current['sunset'] =             time_convert ( data['current']['sunset'], timezone_offset ).strftime("%-I:%M %p")
        current['temp'] =               float(round(data['current']['temp'],1))
        current['feels_like'] =         float(round(data['current']['feels_like'],1))
        current['pressure'] =           data['current']['pressure']/10
        current['humidity'] =           data['current']['humidity']
        current['clouds'] =             data['current']['clouds']
        current['description'] =        data['current']['weather'][0]['description']
        current['wind_speed'] =         float(round(data['current']['wind_speed'],1))
        current['wind_deg'] =           data['current']['wind_deg']
        current['wind_direction'] =     degToCompass (data['current']['wind_deg'])
        current['wind_gust'] =          float(round(data['current']['wind_gust'],1))
    return current

def pop (response):
    pofp = []

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']
        for minute in data['minutely']:
            minutes = {}
            minutes['time'] = time_convert ( minute['dt'], timezone_offset ).strftime("%-I:%M %p")
            minutes['precipitation'] = minute['precipitation']
            pofp.append (minutes)
    return pofp