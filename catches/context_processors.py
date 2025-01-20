from django.conf import settings
from datetime import date

def week_context(request):
    today = date.today()
    weekID = int(today.strftime("%U")) - 12
    if weekID > 13 and weekID <49:
        return {'weekID': weekID}
    else:
        return {'weekID': 0} 