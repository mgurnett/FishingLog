from catches.models import *

def collect_districts_from_lakes():
    lakes = Lake.objects.all()
    print (f"total lakes - {lakes.count()}")
    data = []
    for lake in lakes:
        if lake.district:
            data.append(lake.district)
        else:
            data.append("unknown")
    data_list = set(data)
    return list(sorted(data_list))

def run():
    data = collect_districts_from_lakes() #go get all the districts
    dist_dict = ()
    for i, d in enumerate(data):
        dist_dict=dist_dict + (i, d)
    # print (dist_dict)
    c=0
    for d in dist_dict:
        if isinstance(d, str):
            print (f'({c},"{d}"),')
        else:
            c=d