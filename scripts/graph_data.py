import csv
from catches.models import *
from catches.views import *

    
def run():
    graph_data = collect_tw_from_logs_and_hatches()
    for data in graph_data:
        print (type(graph_data))

    field_names= ['week', 'log', 'week_id', 'temp_id', 'temp', 'temp_name', 'date', 'type']
    with open('graph_data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(graph_data)