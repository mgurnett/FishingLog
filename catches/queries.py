from .models import *
from django.db.models import Q

def convert_user_to_profile (user):
    return Profile.objects.get (user = user)

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

def get_hl (id): 
    temp_list = get_temps(id)
    # print (f'id is {id}   and temp_list is {temp_list}')
    low = 100
    high = 0
    for temp in temp_list:
        if temp['temp'] < low:
            low = temp['temp']
        if temp['temp'] > high:
            high = temp['temp']
    # print (f'low: {low} high: {high}')
    if low == 100:
        return {"low": '', "high": ''}
    else:
        return {"low": low, "high": high}

def fly_list(id):
    # id = 8
    logs = Log.objects.filter(week = id)
    fly_list = []
    for log in logs:
        if log.fly:
            fly_list.append(log.fly)
    fly_list = list(dict.fromkeys(fly_list))
    return fly_list

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
  
def favorite_filter_for_lake (lake_id, current_user) -> int:
    # print (f'{lake_id = }{current_user.id = }')
    try:
        fav = Favorite.objects.get(lake=lake_id, user=current_user.id)
    except:
        fav = None
    else:
        # print (f'{fav = }{fav.id = }')
        return fav.id
  
def log_filter_for_private (log_list, current_user):
        object_list = log_list.filter(Q(private=False) | Q(angler=current_user))
        return object_list

def get_regions_with_lake_for_current_user (lake_id, current_user):
    """
    This function retrieves a queryset of regions containing a specific lake for the current user.

    Args:
        lake_id: The ID of the lake to search for.

    Returns:
        A queryset of Region objects that contain the specified lake and belong to the current user.
    """

    return Region.objects.filter(
        lakes__id=lake_id,  # Filter regions by lake ID
        profile__user=current_user  # Filter by current user through profile
    )

def get_lakes_for_user_by_region (region, current_user):
    """
    This function retrieves a queryset of lakes for a specific user and region.

    Args:
        user: The User object for whom to find lakes.

    Returns:
        A queryset of Lake objects that belong to regions associated with the user.
    """

    return Lake.objects.filter(
        Q(region__profile__user=current_user),  # Filter by user through profile and region
        region=region,  # Filter regions by lake ID
    ).distinct()

