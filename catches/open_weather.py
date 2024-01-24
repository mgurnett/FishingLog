import requests
from zoneinfo import ZoneInfo
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

def current (lake):
    current = {}
    response = requests.get( make_url (float(round(lake.lat,4)), float(round(lake.long,4))) )

    if response.status_code == 200:
        data = response.json()
        current['timezone'] =           data['timezone']
        current['timezone_offset'] =    data['timezone_offset']
        current['time_taken'] =         data['current']['dt'] + data['timezone_offset']
        current['sunrise'] =            data['current']['sunrise'] + data['timezone_offset']
        current['sunset'] =             data['current']['sunset'] + data['timezone_offset']
        current['temp'] =               float(round(data['current']['temp'],1))
        current['feels_like'] =         float(round(data['current']['feels_like']))
        current['pressure'] =           data['current']['pressure']
        current['humidity'] =           data['current']['humidity']
        current['clouds'] =             data['current']['clouds']
        current['wind_speed'] =         float(round(data['current']['wind_speed']))
        current['wind_deg'] =           data['current']['wind_deg']
        current['wind_direction'] =     degToCompass (data['current']['wind_deg'])
    return current