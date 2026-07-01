import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishingLog.settings")
django.setup()

try:
    from easyaudit.models import CRUDEvent
    events = list(CRUDEvent.objects.all()[:10])
    for event in events:
        print(event.datetime)
    print("Successfully loaded events.")
except Exception as e:
    import traceback
    traceback.print_exc()

