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
    return requests.get( make_url (float(round(lake.lat,4)), float(round(lake.long,4))) )

def time_convert (time, offset):
    return datetime.fromtimestamp( time + offset )
    
def get_moon_phase_info(val):
    if val == 0 or val == 1:
        return "New Moon", "bi-moon"
    elif 0 < val < 0.25:
        return "Waxing Crescent", "bi-moon-stars"
    elif val == 0.25:
        return "First Quarter", "bi-moon-text"
    elif 0.25 < val < 0.5:
        return "Waxing Gibbous", "bi-moon-stars"
    elif val == 0.5:
        return "Full Moon", "bi-moon-fill"
    elif 0.5 < val < 0.75:
        return "Waning Gibbous", "bi-moon-stars"
    elif val == 0.75:
        return "Last Quarter", "bi-moon"
    else:
        return "Waning Crescent", "bi-moon-stars"

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
        current['icon'] =               data['current']['weather'][0]['icon']  # <-- Extracted current icon code
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
        for minute in data.get('minutely', []):
            index += 1
            percent += minute['precipitation']*100
            if index == 9:
                pofp.append (
                    {'minutes': time_convert ( minute['dt'], timezone_offset ).strftime("%-I:%M %p"), 
                    'precipitation': percent/10}
                    )
                percent = 0
                index = -1
            
        if not pofp:
            return ""

        df = pd.DataFrame(pofp)
        fig = px.area(
            df, 
            x='minutes', 
            y='precipitation', 
            color_discrete_sequence = ['#578D7F'],
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
    else:
        return ""
    return fig.to_html()

def hourly_forcast (response):
    forcast = []

    if response.status_code == 200:
        data = response.json()
        timezone_offset = data['timezone_offset']
        
        previous_pressure = None  # To track the trend line
        
        for hour in data['hourly']:
            hour_forcast = {}
            hour_forcast['forcast_time'] =       time_convert ( hour['dt'], timezone_offset ).strftime("%-I:%M %p")
            hour_forcast['temp'] =               float(round(hour['temp'],1))
            hour_forcast['feels_like'] =         float(round(hour['feels_like'],1))
            
            # --- Extract Hourly POP Here ---
            hour_forcast['pop'] =                int(hour.get('pop', 0) * 100)
            # -------------------------------

            # OpenWeather sends pressure in hPa (e.g., 1013). You divide by 10 for kPa (101.3 kPa).
            current_pressure = hour['pressure'] / 10
            hour_forcast['pressure'] =           current_pressure
            
            # --- Calculate Pressure Trend ---
            if previous_pressure is None:
                hour_forcast['pressure_trend'] = "flat"  # First hour benchmark
            elif current_pressure > previous_pressure:
                hour_forcast['pressure_trend'] = "rising"
            elif current_pressure < previous_pressure:
                hour_forcast['pressure_trend'] = "falling"
            else:
                hour_forcast['pressure_trend'] = "flat"
                
            previous_pressure = current_pressure  # Update benchmark for the next hour block
            # ---------------------------------

            hour_forcast['humidity'] =           hour['humidity']
            hour_forcast['clouds'] =             hour['clouds']
            hour_forcast['description'] =        hour['weather'][0]['description']
            hour_forcast['icon'] =               hour['weather'][0]['icon']
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
            daily_forcast['pop'] =                int(day['pop']*100)
            daily_forcast['description'] =        day['weather'][0]['description']
            daily_forcast['icon'] =               day['weather'][0]['icon']  # <-- Extracted daily icon code
            daily_forcast['wind_speed'] =         float(round(day['wind_speed'],1))
            daily_forcast['wind_deg'] =           day['wind_deg']
            daily_forcast['wind_direction'] =     degToCompass (day['wind_deg'])
            phase_name, phase_icon = get_moon_phase_info(day['moon_phase'])
            daily_forcast['moon_phase_name'] = phase_name
            daily_forcast['moon_phase_icon'] = phase_icon
            try:
                daily_forcast['wind_gust'] =      float(round(day['wind_gust'],1))
            except:
                daily_forcast['wind_gust'] = 0
            forcast.append(daily_forcast)
    return forcast

