from catches/models import *

def get_query_set(*args, **kwargs): 

    week_data = Week.objects.get(id=kwargs['pk'])
    last_week = week_data.prev_num
    next_week = week_data.next_num
    
    chart_now = Chart.objects.filter (week=week_data.id)
    chart_last = Chart.objects.filter (week=last_week)
    chart_next = Chart.objects.filter (week=next_week)
    
    three_charts = []
    for index, c in enumerate(chart_now):
        print (f'#{index} - {c.bug.name} last {chart_last[index].strength} this {c.strength} next {chart_next[index].strength}')
        insect = [ 
            # bug: c.bug, 
            # last_strength: chart_last[index].strength, 
            # last_strength: c.strength,
            # next_strength: chart_next[index].strength,
            c, 
            chart_last[index], 
            chart_next[index],
            ]
        three_charts.append(insect)
    return three_charts
    # context ['chart_for_last_week'] = Chart.objects.filter (week=last_week).order_by('-strength')
    # context ['chart_for_week'] = Chart.objects.filter (week=this_week).order_by('-strength')
    # context ['hatches'] = Hatch.objects.filter (week=self.kwargs['pk']).order_by('temp')
    # context ['temps'] = Temp.objects.filter (week=self.kwargs['pk']).order_by('id')
    # context ['logs'] = Log.objects.filter (week=self.kwargs['pk'])
    # return context
    
def run():
    week_data = Week.objects.get(number=30)
    chart_list = get_query_set(pk = week_data.id)
    print (chart_list)
