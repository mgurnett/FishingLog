import asyncio
from env_canada import ECWeather
from zoneinfo import ZoneInfo
    
localtz = ZoneInfo('America/Edmonton')
utc = ZoneInfo('UTC')

def get_alerts(data):
    # print (data)
    title = ""
    alert_type = ""
    date = ""
    colour = "#000000"

    endings = data.get('endings')
    if endings.get('value'):
        title = endings.get('value')[0].get('title')
        alert_type = "ending"
        date = endings.get('value')[0].get('date')
        colour = "#66CC66"

    statements = data.get('statements')
    if statements.get('value'):
        title = statements.get('value')[0].get('title')
        alert_type = "statement"
        date = statements.get('value')[0].get('date')
        colour = "#707070"

    advisories = data.get('advisories')
    if advisories.get('value'):
        title = advisories.get('value')[0].get('title')
        alert_type = "advisory"
        date = advisories.get('value')[0].get('date')
        colour = "#707070"

    watches = data.get('watches')
    if watches.get('watches'):
        title = watches.get('value')[0].get('title')
        alert_type = "warning"
        date = watches.get('value')[0].get('date')
        colour = "#FFFF00"
        
    warnings = data.get('warnings')
    if warnings.get('value'):
        # print (f"This is a warning {warnings}")
        title = warnings.get('value')[0].get('title')
        alert_type = "warning"
        date = warnings.get('value')[0].get('date')
        colour = "#BB0000"

    data_dict = {'alert_type': alert_type, 'title': title, 'date': date, 'colour': colour }
        
    return data_dict

def weather_data (lake):
    # print ("starting weather")
    current_conditions = {}
    ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    try:
        asyncio.run(ec_en.update())
    except:
        current_conditions = ""
    else:  
        current_dict = {}

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
                    current_dict [label] = value  #add the lable and the value to the current conditions
            # if value !="" and value != None:
            #     print (f'{label}: {value}')
        
        sunrise_time = current_dict.get("sunrise")
        utctime = sunrise_time.replace(tzinfo=utc)
        sunrise_time_local = utctime.astimezone(localtz).strftime("%-I:%M %p")
        # print (f'sunrise_time is: {sunrise_time.strftime("%-I:%M %p")} and sunrise_time_local is {sunrise_time_local}')

        sunset_time = current_dict.get("sunset")
        utctime = sunset_time.replace(tzinfo=utc)
        sunset_time_local = utctime.astimezone(localtz).strftime("%-I:%M %p")

        current_conditions ["temperature"] = current_dict.get("temperature")
        current_conditions ["humidex"] = current_dict.get("humidex")
        current_conditions ["pressure"] = current_dict.get("pressure")
        current_conditions ["tendency"] = current_dict.get("tendency")
        current_conditions ["humidity"] = current_dict.get("humidity")
        current_conditions ["sunrise"] = sunrise_time_local
        current_conditions ["sunset"] = sunset_time_local
        current_conditions ["alerts"] = get_alerts (ec_en.alerts)
    finally:
        # print ("Current conditions" + current_conditions)
        return current_conditions #<class 'dict'>

def five_day_forcast (lake):
    ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    # ec_en = ECWeather(coordinates=(53.53, -113.49))
    asyncio.run(ec_en.update())
    five_forecast = []
    for x in range (0,5):
        hour_forecast_dict = {}
        hour_forecast = ec_en.hourly_forecasts[x].get('period')
        utctime = hour_forecast.replace(tzinfo=utc)
        localtime = utctime.astimezone(localtz)
        hour_forecast_dict = { 
            # 'fore_time': localtime.strftime("%a, %b %-d at %-I:%M %p"),
            'fore_time': localtime.strftime("%-I:%M %p"),
            'conditions': ec_en.hourly_forecasts[x].get('condition'),
            'temperature': ec_en.hourly_forecasts[x].get('temperature'),
            'pop': ec_en.hourly_forecasts[x].get('precip_probability'),
            'icon': ec_en.hourly_forecasts[x].get('icon_code'),
            }
        # print (hour_forecast_dict)
        five_forecast.append(hour_forecast_dict)
        # print (five_forecast)
    return five_forecast

        # print (f'Forecast for the hour of {fore_time} there will be a {conditions}' + \
        #     f' with a temperature of {temperature}C and a {precip_probability}% chance of precipitation')

    #Icon code can be downloaded from: https://meteo.gc.ca/weathericons/09.gif