from catches.models import *

def run():
    all_weeks = Week.objects.all()
    for week in all_weeks:
        total_temp = 0
        n = 0
        for log in Log.objects.filter(week=week):
            if log.temp.deg > 0:
                total_temp += log.temp.deg
                n += 1
        if n > 0:
            temp_average = int(total_temp / n)
        else:
            temp_average = 0
        print (f'{week} with an average temp of {temp_average}')
        week.ave_temp = temp_average
        week.save()

