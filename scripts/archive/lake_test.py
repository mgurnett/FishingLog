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
    ('Ethel Lake', 'EL'),
    ('Graham Lake', 'GL'),
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
    ('EL', 'Ethel Lake'),
    ('GL', 'Graham Lake'),
)
FILE_NAME = 'extra files/epa-alberta-fish-stocking-report-2025.csv'

def run():
    
    with open(FILE_NAME) as file:
        numline = len(file.readlines()) - 1   # not accurate because of the \n s in the file.

    line_count = 0
    with open(FILE_NAME) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        total_fish_stocked = 0
        total_trout_stocked = 0
        total_non_trout_stocked = 0
        for stock_count, row in enumerate(reader):
            line_count += 1
            # print (row)
            try:  # check to see if we have the lake in the database already
                lake_id = Lake.objects.get(ats=row[2])
                # print (lake_id)
            except Exception as e:
                print (f'LAKE missing: {row[0]} ({row[1]} ATS: {row[2]}) | Error details: {e}')

            # print (f'{stock_count+2} - {stock}')
            percent = round(line_count/numline*100,1)
            print (f'Line count: {line_count} of {numline} or {percent}% | {total_trout_stocked:,} trout stocked and {total_non_trout_stocked:,} non-trout stocked', end="\r")
        print (f'{total_trout_stocked:,} trout stocked and {total_non_trout_stocked:,} non-trout stocked for a total of {total_fish_stocked:,}')

        '''
        https://www.ilovepdf.com/pdf_to_excel
        Set stock number to have no comma
        Set date to dd-mm-yyyy
        Remove the top row - blank
        python3 manage.py runscript stock_import_2025
        '''
