from catches.models import *
import re
from datetime import datetime
import csv

# https://www.adobe.com/acrobat/online/pdf-to-excel.html

STRAIN_lookup = [
    ('Beitty x Beitty', 'BEBE'),
    ('Beitty Resort', 'BEBE'),
    ('Bow River x Beitty', 'BRBE'),
    ('Campbell Lake', 'CLCL'),
    ('Lyndon', 'LYLY'),
    ('Pit Lake', 'PLPL'),
    ('Pit Lakes', 'PLPL'),
    ('Trout Lodge / Jumpers', 'TLTLJ'),
    ('Trout Lodge/Jumpers', 'TLTLJ'),
    ('Trout Lodge / Kamloops', 'TLTLK'),
    ('Trout Lodge/Kamloops', 'TLTLK'),
    ('Trout Lodge/Kamloops', 'TLTLK'),
    ('Trout Lodge / Silvers', 'TLTLS'),
    ("Trout Lodge/Silver's", 'TLTLS'),
    ('Bow River', 'BRBE'),
    ('Beitty/Bow River', 'BRBE'),
    ('Lac Ste. Anne', 'LSE'),
    ('Job Lake', 'JBL'),
    ('Allison Creek', "AC"),
    ('Riverence', "RD"),
    ('Marie Creek', 'MC'),
    ('Rock Island', 'RI'),
 ]
STRAIN = (
    ("BEBE", "Beitty x Beitty"),
    ("BRBE", "Bow River x Beitty"),
    ("CLCL", "Campbell Lake"),
    ("LYLY", "Lyndon"),
    ("PLPL", "Pit Lake"),
    ("TLTLJ", "Trout Lodge / Jumpers"),
    ("TLTLK", "Trout Lodge / Kamloops"),
    ("TLTLS", "Trout Lodge / Silvers"),
    ("LSE", "Lac Ste. Anne"),
    ("JBL", "Job Lake"),
    ("AC", 'Allison Creek'),
    ("RD", 'Riverence'),
    ("MC", 'Marie Creek'),
    ("RI", 'Rock Island'),
)


def run():
    Stock.objects.filter(date_stocked__year=2024).delete()

    with open('extra files/stockreport as of June 4.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        total_fish_stocked = 0
        for stock_count, row in enumerate(reader):
            # print (row)
            try:  # check to see if we have the lake in the database already
                lake_id = Lake.objects.get(ats=row[2])
                # print (lake_id)
            except:
                print (f'LAKE missing: {row[0]} ({row[1]})')

            try:  # check to see if we have the fish in the database already
                fish_id = Fish.objects.get(abbreviation=row[3])
            except:
                # print (f'We are looking for {row[3]} and we failed')
                print (f'FISH missing: {row[3]} from Lake: {row[0]} ({row[1]}')

            found=0
            strain = ""
            for index, str_look in enumerate(STRAIN_lookup):
                if row[4] == str_look[0]:
                    found=index
            if found == 0:
                # print (f'We are going to look for {row[4]} in lake {lake_id} with fish {fish_id}')
                # print (row)
                print (f'STRAIN missing: {row[4]} from Lake: {row[0]} ({row[1]}')
            else:
                strain = STRAIN_lookup[found][1]

            if row[5] in ("2N", "3N", "AF2N", "AF3N"):
                geo = row[5]
            else:
                geo = ""

            # Date convert
            date_object = datetime.strptime(str(row[8]), '%d-%b-%y').date()
            date_object_iso = date_object.isoformat()

            # print(f'{date_object = } | {type(date_object) = } | {date_object_iso = } | {type(date_object_iso) = }')
            # print(f'{date_object.date.isoformat() = }')
            # print(date_object.isoformat())
            # print(f'{date_object.isoformat() = }')

            stock = Stock (
                date_stocked = date_object,
                number = row[7],
                length = row[6],
                lake = lake_id,
                fish = fish_id,
                strain = strain,
                gentotype = geo,
                )
            total_fish_stocked += int(row[7])
            # print (f'{stock_count+2} - {stock}')
            stock.save()
            print (f'{stock_count+2} - {stock}')
        print (f'total number of fish stocked is: {total_fish_stocked}')