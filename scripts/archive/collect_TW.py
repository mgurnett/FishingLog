from catches.models import *
import pandas as pd

def collect_tw_from_logs_and_hatches():
    logs = Log.objects.all()
    hatches = Hatch.objects.all()
    data = []
    for log in logs:
        if log.temp.id > 1:
            log_data = {'week': log.week.number, 'date': log.catch_date, 'temp': log.temp.deg, 'temp_name': log.temp.name}
            data.append(log_data)
    for hatch in hatches:
        if hatch.temp.id > 1:
            log_data = {'week': hatch.week.id, 'temp': hatch.temp.id}
            data.append(log_data)
    return data

def run():
    data = collect_tw_from_logs_and_hatches()
    # print (data)

    df = pd.DataFrame.from_dict( data )
    df.columns = ['Week', 'Catch date', 'Temperature', 'Temperature Name']
    

    print (df.sort_values(by='Week'))
