import asyncio
from env_canada import ECWeather
from zoneinfo import ZoneInfo
    
localtz = ZoneInfo('America/Edmonton')
utc = ZoneInfo('UTC')

def get_alerts(data):
    title = ""
    alert_type = ""
    date = ""
    colour = "#000000"

    if not data:
        return {'alert_type': alert_type, 'title': title, 'date': date, 'colour': colour }

    endings = data.get('endings', {})
    if endings and endings.get('value'):
        title = endings.get('value')[0].get('title')
        alert_type = "ending"
        date = endings.get('value')[0].get('date')
        colour = "#66CC66"

    statements = data.get('statements', {})
    if statements and statements.get('value'):
        title = statements.get('value')[0].get('title')
        alert_type = "statement"
        date = statements.get('value')[0].get('date')
        colour = "#707070"

    advisories = data.get('advisories', {})
    if advisories and advisories.get('value'):
        title = advisories.get('value')[0].get('title')
        alert_type = "advisory"
        date = advisories.get('value')[0].get('date')
        colour = "#707070"

    watches = data.get('watches', {})
    if watches and watches.get('value'):
        title = watches.get('value')[0].get('title')
        alert_type = "warning"
        date = watches.get('value')[0].get('date')
        colour = "#FFFF00"
        
    warnings = data.get('warnings', {})
    if warnings and warnings.get('value'):
        title = warnings.get('value')[0].get('title')
        alert_type = "warning"
        date = warnings.get('value')[0].get('date')
        colour = "#BB0000"

    data_dict = {'alert_type': alert_type, 'title': title, 'date': date, 'colour': colour }
    return data_dict

def weather_data (lake):
    current_conditions = {}
    ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    try:
        asyncio.run(ec_en.update())
    except:
        current_conditions = ""
    else:  
        current_dict = {}

        for measurement in ec_en.conditions:
            label = str(ec_en.conditions[measurement].get('label', '')).lower()
            if not label:
                continue
            try:
                value = ec_en.conditions.get(label, {}).get('value')
            except:
                value = ""
            else:
                if value is not None:
                    current_dict [label] = value
        
        sunrise_time = current_dict.get("sunrise")
        if sunrise_time:
            try:
                utctime = sunrise_time.replace(tzinfo=utc)
                sunrise_time_local = utctime.astimezone(localtz).strftime("%-I:%M %p")
            except:
                sunrise_time_local = ""
        else:
            sunrise_time_local = ""

        sunset_time = current_dict.get("sunset")
        if sunset_time:
            try:
                utctime = sunset_time.replace(tzinfo=utc)
                sunset_time_local = utctime.astimezone(localtz).strftime("%-I:%M %p")
            except:
                sunset_time_local = ""
        else:
            sunset_time_local = ""

        current_conditions ["temperature"] = current_dict.get("temperature")
        current_conditions ["humidex"] = current_dict.get("humidex")
        current_conditions ["pressure"] = current_dict.get("pressure")
        current_conditions ["tendency"] = current_dict.get("tendency")
        current_conditions ["humidity"] = current_dict.get("humidity")
        current_conditions ["sunrise"] = sunrise_time_local
        current_conditions ["sunset"] = sunset_time_local
        current_conditions ["alerts"] = get_alerts (ec_en.alerts)
    finally:
        return current_conditions

def five_day_forcast (lake):
    ec_en = ECWeather(coordinates=(float(round(lake.lat,2)), float(round(lake.long,2))))
    five_forecast = []
    try:
        asyncio.run(ec_en.update())
    except:
        pass
    else:
        if ec_en.hourly_forecasts:
            for x in range (0, min(5, len(ec_en.hourly_forecasts))):
                hour_forecast_dict = {}
                hour_forecast = ec_en.hourly_forecasts[x].get('period')
                if hour_forecast:
                    try:
                        utctime = hour_forecast.replace(tzinfo=utc)
                        localtime = utctime.astimezone(localtz)
                        hour_forecast_dict = { 
                            'fore_time': localtime.strftime("%-I:%M %p"),
                            'conditions': ec_en.hourly_forecasts[x].get('condition'),
                            'temperature': ec_en.hourly_forecasts[x].get('temperature'),
                            'pop': ec_en.hourly_forecasts[x].get('precip_probability'),
                            'icon': ec_en.hourly_forecasts[x].get('icon_code'),
                            }
                        five_forecast.append(hour_forecast_dict)
                    except:
                        pass
    return five_forecast
