from catches.models import *
import re
from datetime import datetime
import csv
import string


FILE_NAME = 'extra files/regslist.csv'

def run():
    with open(FILE_NAME) as file:
        numline = len(file.readlines()) - 1
    line_count = 0
    with open(FILE_NAME) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        total_lakes_matched = 0
        total_lakes_unmatched = 0
        for row in reader:
            line_count += 1
            ats_string = row[4].replace(" ", "")
            # print (f'{row[4] = } and {ats_string = }')
            # print (row)
            try:  # check to see if we have the lake in the database already
                lake = Lake.objects.get(ats=ats_string)
                # print (f'LAKE found: {lake.name = } at {ats_string = }')
                lake.reg_location = row[1]
                total_lakes_matched +=1
            except:
                print (f'LAKE missing: {row[0]} ({row[1]})')
                total_lakes_unmatched +=1

            lake.save()
            percent = round(line_count/numline*100,1)
            # print (f'Line count: {line_count} of {numline} or {percent}% | Lakes found: {total_lakes_matched:,} Lakes missed {total_lakes_unmatched:,}', end="\r")
            print (f'Lake: {lake} of {row[1]}')
        print (f'Lakes found: {total_lakes_matched:,} Lakes missed {total_lakes_unmatched:,}')