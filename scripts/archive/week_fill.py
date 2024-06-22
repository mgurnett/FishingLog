from catches.models import *

def run():

    logs = Log.objects.all()
    for log in logs:
        week_num = int(log.catch_date.strftime('%U'))
        week = Week.objects.get(number = week_num)
        if not log.week:
            log.week = week
            log.save()
        
        print (f'week = {week} log.week = {log.week}')
        


