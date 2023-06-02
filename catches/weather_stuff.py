import asyncio
from env_canada import ECWeather
from zoneinfo import ZoneInfo
    
localtz = ZoneInfo('America/Edmonton')
utc = ZoneInfo('UTC')

def weather_data (lake):
    ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    # ec_en = ECWeather(coordinates=(53.53, -113.49))
    asyncio.run(ec_en.update())
    current_conditions = {}

    for measurement in ec_en.conditions:  #go through all lines of the current condition
        label = str(ec_en.conditions[measurement].get('label')).lower() #grab the lables.
        # print (label)
        try:
            value = ec_en.conditions.get(label).get('value') #see if you can get the value for that label
        except:
            value = "" # if not, disreguard 
        else:
            # print (type(value))
            if value != None: #as long as its not a Classtype None
                current_conditions [label] = value  #add the lable and the value to the current conditions
    return current_conditions #<class 'dict'>

def five_day_forcast (lake):   

    # ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    ec_en = ECWeather(coordinates=(53.53, -113.49))
    asyncio.run(ec_en.update())
    five_forecast = []
    for x in range (0,5):
        hour_forecast_dict = {}
        hour_forecast = ec_en.hourly_forecasts[x].get('period')
        utctime = hour_forecast.replace(tzinfo=utc)
        localtime = utctime.astimezone(localtz)
        hour_forecast_dict = { 
            'fore_time': localtime.strftime("%a, %b %-d at %-I:%M %p"),
            'conditions': ec_en.hourly_forecasts[x].get('condition'),
            'temperature': ec_en.hourly_forecasts[x].get('temperature'),
            'pop': ec_en.hourly_forecasts[x].get('precip_probability'),
            }
        five_forecast.append(hour_forecast_dict)
        # print (five_forecast)
    return five_forecast

        # print (f'Forecast for the hour of {fore_time} there will be a {conditions}' + \
        #     f' with a temperature of {temperature}C and a {precip_probability}% chance of precipitation')

    #Icon code can be downloaded from: https://meteo.gc.ca/weathericons/09.gif