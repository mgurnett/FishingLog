import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishingLog.settings")
django.setup()

from catches.models import Lake

try:
    lake = Lake.objects.first()
    if lake:
        # Just save it to trigger Easy Audit's post_save signal
        lake.save()
        print("Lake saved, Easy Audit should have logged it.")
    else:
        print("No lake found")
except Exception as e:
    import traceback
    traceback.print_exc()

