from .models import *
from django.db.models import Q

def collect_tw_from_logs_and_hatches(**kwargs):
    lake = kwargs.pop('lake', '')
    if lake:
        logs = Log.objects.filter(lake=lake)
        hatches = Hatch.objects.filter(lake=lake)
    else:
        logs = Log.objects.all()
        hatches = Hatch.objects.all() 
    data = []
    for log in logs:
        if log.temp.id > 1:
            log_data = {
                'week': log.week.number, 
                'week_id': log.week.id, 
                'date': log.catch_date, 
                'temp': log.temp.deg,
                'temp_id': log.temp.id, 
                'temp_name': log.temp.name, 
                'log': log.id,
                'type': 'L'
                }
            data.append(log_data)

    for hatch in hatches:
        if hatch.temp:
            if hatch.temp.id > 1:
                log_data = {
                    'week': hatch.week.number, 
                    'week_id': hatch.week.id, 
                    'date': hatch.sight_date, 
                    'temp': hatch.temp.deg,
                    'temp_id': hatch.temp.id, 
                    'temp_name': hatch.temp.name, 
                    'log': hatch.id,
                    'type': 'H'
                    }
                data.append(log_data)
    return data  #  list of dictionaries 

def get_query_set(pk): # get the data for the hatch trends for week detail view

    try:
        week_data = Week.objects.get(id=pk)
    except:
        allcharts = []
        return allcharts

    last_week = week_data.prev_num
    next_week = week_data.next_num
    
    chart_now = Chart.objects.filter (week=week_data.id)
    chart_last = Chart.objects.filter (week=last_week)
    chart_next = Chart.objects.filter (week=next_week)
    
    three_charts = []
    for index, c in enumerate(chart_now):
        if chart_last[index].strength + c.strength < c.strength + chart_next[index].strength:
            trend = "rising"
        elif chart_last[index].strength + c.strength == c.strength + chart_next[index].strength:
            trend = "flat"
        elif chart_last[index].strength + c.strength > c.strength + chart_next[index].strength:
            trend = "falling"
        insect = {
                    'bug': c.bug.name, 
                    'bug_id': c.bug.id,
                    'last': chart_last[index].strength_name, 
                    'this': c.strength_name,
                    'next': chart_next[index].strength_name,
                    'trend': trend,
                    'strength': c.strength
                }

        three_charts.append(insect)
    allcharts = sorted(three_charts, key=lambda d: d['strength'], reverse=True)
    allcharts = sorted(allcharts, key=lambda d: d['trend'], reverse=True)

    return allcharts

def get_temps(pk):
    all_temps = collect_tw_from_logs_and_hatches()
    temps_this_week = []
    for temp in all_temps:
        if temp.get("week_id") == pk:
            temps_this_week.append(temp)
    temp_list = sorted (temps_this_week, key=lambda d: d['temp_name'], reverse=True)
    return temp_list

def get_weeks(pk):
    all_weeks = collect_tw_from_logs_and_hatches()
    weeks_this_temp = []
    for week in all_weeks:
        if week.get("temp_id") == pk:
            weeks_this_temp.append(week)
    week_list = sorted (weeks_this_temp, key=lambda d: d['week'], reverse=True)
    return week_list
  
def log_filter_for_private (log_list, current_user):
        object_list = log_list.filter(Q(private=False) | Q(angler=current_user))
        return object_list