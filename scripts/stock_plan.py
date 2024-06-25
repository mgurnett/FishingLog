from catches.models import *
import csv
from catches.fish_data import DISTRICTS

def find_dist_num (dists, name):
    for d in dists:
        if name == d[1]:
            return d[0]
    return 60

def check_lake_name (name):
    lake_list = Lake.objects.filter (name = name)
    return lake_list

def check_lake_lat (lat, long):
    lake_list = Lake.objects.filter (lat__contains = lat) | Lake.objects.filter (long__contains = long)
    return lake_list

def run():
    dists = list(DISTRICTS)
    with open('extra files/epa-fish-stocking-planned-dates-2024.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        index=0
        for row in reader:
            lake_list_n = check_lake_name (row[1])
            if not lake_list_n:
                lat_to_check = round(float(row[2]),6)
                long_to_check = round(float(row[3]),6)
                lake_list_lat = check_lake_lat (lat_to_check, long_to_check)
                if not lake_list_lat:
                    # print (f'{row = } {lat_to_check = } {lake_list_lat = }')
                    index += 1
                    # print (f'{index} - {row = }')
                    dist_num = find_dist_num (dists, row[0])
                    lake = Lake (
                        name = row[1],
                        district = dist_num,
                        lat = lat_to_check,
                        long = long_to_check
                    )
                    print (f'{lake = }')
                    lake.save()