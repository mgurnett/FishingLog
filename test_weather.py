import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishingLog.settings")
django.setup()

from catches.models import Log, Lake, Fish, Temp, Week
from django.contrib.auth.models import User
import datetime
from catches.models import LogWeather

# Find latest log
log = Log.objects.order_by('-id').first()
if not log:
    print("No logs found.")
    exit()

print(f"Latest Log ID: {log.id}")
print(f"Date: {log.catch_date}, Time: {log.catch_time}")
print(f"Lat: {log.gps_lat}, Lon: {log.gps_long}")
print(f"Has weather? {hasattr(log, 'weather')}")

if hasattr(log, 'weather'):
    print(f"Weather temp: {log.weather.temp}")
else:
    # Try triggering it manually
    print("Triggering weather fetch manually...")
    from catches.models import fetch_weather_for_log
    fetch_weather_for_log(Log, log, False)
    
    # Reload log
    log.refresh_from_db()
    print(f"Has weather now? {hasattr(log, 'weather')}")
    if hasattr(log, 'weather'):
        print(f"Weather temp: {log.weather.temp}")
