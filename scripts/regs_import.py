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
                total_lakes_matched +=1
            except:
                print (f'LAKE missing: {row[0]} ({row[1]})')
                total_lakes_unmatched +=1

            # try:  # check to see if we have the fish in the database already
            #     fish_id = Fish.objects.get(abbreviation=row[3])
            #     if fish_id.id in [7,8,9,10,14]:
            #         total_non_trout_stocked += int(row[7])
            #     else:
            #         total_trout_stocked += int(row[7])

            # except:
            #     # print (f'We are looking for {row[3]} and we failed')
            #     print (f'FISH missing: {row[3]} from Lake: {row[0]} ({row[1]}')

            # found=0
            # strain = ""
            # for index, str_look in enumerate(STRAIN_lookup):
            #     if row[4] == str_look[0]:
            #         found=index
            # if found == 0:
            #     # print (f'We are going to look for {row[4]} in lake {lake_id} with fish {fish_id}')
            #     # print (row)
            #     print (f'STRAIN missing: {row[4]} from Lake: {row[0]} ({row[1]}')
            # else:
            #     strain = STRAIN_lookup[found][1]

            # if row[5] in ("2N", "3N", "AF2N", "AF3N"):
            #     geo = row[5]
            # else:
            #     geo = ""

            # # Date convert
            # try:
            #     date_object = datetime.strptime(str(row[8]), '%d-%b-%y').date() #dd-mm-yyyy
            # except:
            #     date_object = datetime.strptime(str(row[8]), '%Y-%m-%d').date() #yyyy-mm-dd


            # stock = Stock (
            #     date_stocked = date_object,
            #     number = row[7],
            #     length = row[6],
            #     lake = lake_id,
            #     fish = fish_id,
            #     strain = strain,
            #     gentotype = geo,
            #     )
            # total_fish_stocked += int(row[7])
            # # print (f'{stock_count+2} - {stock}')
            # stock.save()
            # # print (f'{stock_count+2} - {stock}')
            percent = round(line_count/numline*100,1)
            print (f'Line count: {line_count} of {numline} or {percent}% | Lakes found: {total_lakes_matched:,} Lakes missed {total_lakes_unmatched:,}', end="\r")
        print (f'Lakes found: {total_lakes_matched:,} Lakes missed {total_lakes_unmatched:,}')