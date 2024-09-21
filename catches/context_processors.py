from django.conf import settings
from datetime import date

def week_context(request):
    today = date.today()
    weekID = int(today.strftime("%U")) - 12
    return {'weekID': weekID}