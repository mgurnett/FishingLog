import requests
from zoneinfo import ZoneInfo
from datetime import datetime
from django.conf import settings
import pandas as pd
import plotly.express as px
    
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
        try:
            current['wind_gust'] =          float(round(data['current']['wind_gust'],1))
        except:
            current['wind_gust'] = 0
    return current

def temp_graph (response):
    pofp = []

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']
        index = -1
        percent = 0
        for minute in data['minutely']:
            index += 1
            percent += minute['precipitation']
            if index == 9:
                pofp.append (
                    {'minutes': time_convert ( minute['dt'], timezone_offset ).strftime("%-I:%M %p"), 
                    'precipitation': percent/10}
                    )
                percent = 0
                index = -1
            
        df = pd.DataFrame(pofp)
        first_time = df['minutes'].iloc[0]
        last_time = df['minutes'].iloc[-1]
        print (f'{first_time} and {last_time}')

        fig = px.area(
            df, 
            x='minutes', 
            y='precipitation', 
            color_discrete_sequence = ['#578D7F'],
            # title='percentage of precipitation', 
            )
        fig.update_layout(
            height=200,
            paper_bgcolor='#A3C3BF',
            plot_bgcolor='#A3C3BF',
            )
        fig.update_xaxes(
            gridcolor='#A3C3BF',
            tickformat="%-I:%-M",     
            )
        fig.update_yaxes(
            gridcolor='#A3C3BF',
            range = [0, 100],
            )
    # https://plotly.com/python/reference/layout/yaxis/
    else:
        return ""
    return fig.to_html()

def hourly_forcast (response):
    forcast = []

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']
        for hour in data['hourly']:
            hour_forcast = {}
            hour_forcast['forcast_time'] =         time_convert ( hour['dt'], timezone_offset ).strftime("%-I:%M %p")
            hour_forcast['temp'] =               float(round(hour['temp'],1))
            hour_forcast['feels_like'] =         float(round(hour['feels_like'],1))
            hour_forcast['pressure'] =           hour['pressure']/10
            hour_forcast['humidity'] =           hour['humidity']
            hour_forcast['clouds'] =             hour['clouds']
            hour_forcast['description'] =        hour['weather'][0]['description']
            hour_forcast['wind_speed'] =         float(round(hour['wind_speed'],1))
            hour_forcast['wind_deg'] =           hour['wind_deg']
            hour_forcast['wind_direction'] =     degToCompass (hour['wind_deg'])
            try:
                hour_forcast['wind_gust'] =      float(round(hour['wind_gust'],1))
            except:
                hour_forcast['wind_gust'] = 0
            forcast.append(hour_forcast)
    return forcast

def daily_forcast (response):
    forcast = []

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']
        for day in data['daily']:
            daily_forcast = {}
            daily_forcast['forcast_time'] =       time_convert ( day['dt'], timezone_offset ).strftime("%a, %b %-d")
            daily_forcast['sunrise'] =            time_convert ( day['sunrise'], timezone_offset ).strftime("%-I:%M %p")
            daily_forcast['sunset'] =             time_convert ( day['sunset'], timezone_offset ).strftime("%-I:%M %p")
            daily_forcast['moon_phase'] =         day['moon_phase']
            daily_forcast['summary'] =            day['summary']
            daily_forcast['temp_hi'] =            float(round(day['temp']['max'],1))
            daily_forcast['temp_low'] =           float(round(day['temp']['min'],1))
            daily_forcast['feels_like'] =         float(round(day['feels_like']['day'],1))
            daily_forcast['pressure'] =           day['pressure']/10
            daily_forcast['humidity'] =           day['humidity']
            daily_forcast['clouds'] =             day['clouds']
            daily_forcast['pop'] =                day['pop']
            daily_forcast['description'] =        day['weather'][0]['description']
            daily_forcast['wind_speed'] =         float(round(day['wind_speed'],1))
            daily_forcast['wind_deg'] =           day['wind_deg']
            daily_forcast['wind_direction'] =     degToCompass (day['wind_deg'])
            try:
                daily_forcast['wind_gust'] =      float(round(day['wind_gust'],1))
            except:
                daily_forcast['wind_gust'] = 0
            # print (daily_forcast)
            forcast.append(daily_forcast)
    return forcast