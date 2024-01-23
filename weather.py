import requests
from datetime import datetime

api_key = 'b0c00848fbb4cb7f70bf7c20d1738246'

lat = 53.5659479
lon = -113.4243562

url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data['current']['temp']
    desc = data['current']['weather'][0]['main']
    curr_time = data['current']['dt'] + data['timezone_offset']
    sun_r = data['current']['sunrise'] + data['timezone_offset']
    current_time = datetime.utcfromtimestamp(curr_time).strftime('%Y-%m-%d %H:%M:%S')
    sunrise = datetime.utcfromtimestamp(sun_r).strftime('%Y-%m-%d %H:%M:%S')

    print(f'Temperature: {temp} C')
    print(f'Description: {desc}')
    print(f'Time: {current_time}')
    print(f'Time: {sunrise}')

    minutely = data['minutely']
    for minute in minutely:
        p_time = minute["dt"] + data["timezone_offset"]
        pop_time = datetime.utcfromtimestamp(p_time).strftime('%Y-%m-%d %H:%M:%S')
        print (f'time: {pop_time} is {minute["precipitation"]}')

    hourly = data['hourly']
    for hour in hourly:
        p_time = hour["dt"] + data["timezone_offset"]
        hourly_time = datetime.utcfromtimestamp(p_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print (f'time: {hourly_time} is {hour["temp"]}C but feels like {hour["feels_like"]}C with a wind of {hour["wind_speed"]}km at {hour["wind_deg"]}deg')
    

else:
    print('Error fetching weather data')
#https://openweathermap.org/forecast5
