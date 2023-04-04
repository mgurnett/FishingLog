import asyncio

from env_canada import ECWeather

ec_en = ECWeather(coordinates=(50, -100))
ec_fr = ECWeather(station_id='AB/s0000045', language='english')

asyncio.run(ec_en.update())

# current conditions
print (ec_en.conditions)

# daily forecasts
ec_en.daily_forecasts

# hourly forecasts
ec_en.hourly_forecasts

# alerts
ec_en.alerts