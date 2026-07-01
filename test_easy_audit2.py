import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishingLog.settings")
django.setup()

from catches.models import Log, Lake, Fish
from django.contrib.auth.models import User
import datetime

user = User.objects.first()
lake = Lake.objects.first()
fish = Fish.objects.first()

try:
    log = Log.objects.create(
        lake=lake,
        angler=user,
        fish=fish,
        gps_lat=51.0,
        gps_long=-114.0,
        catch_date=datetime.date.today(),
        catch_time=datetime.datetime.now().time(),
        fish_swami=0
    )
    print("Log created successfully")
except Exception as e:
    import traceback
    traceback.print_exc()

