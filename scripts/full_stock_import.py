from catches.models import *
import re
from datetime import datetime
import csv
import pandas as pd
from django.db.models import Q


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

def get_data (file_name):
    
    with open(FILE_NAME) as file:
        numline = len(file.readlines()) - 1   # not accurate because of the \n s in the file.

    line_count = 0
    with open(FILE_NAME) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        all_rows_data = []

        for row in reader:
            # Create a dictionary for the current row
            row_data = {
                'Lake Name': row[0],
                'Waterbody Name': row[1],
                'ATS': row[2],
                'Fish Abbreviation': row[3],
                'Strain': row[4],
                'Genotype': row[5],
                'Length': row[6],
                'Number': row[7],
                'Date Stocked': row[8],
            }
            # Append the dictionary to a list
            all_rows_data.append(row_data)

        # Create a DataFrame from the list of dictionaries
        return pd.DataFrame(all_rows_data)

def check_lakes_with_name_transfer_logic(df):
    for row in df.itertuples(index=False):
        
        # Clean the input data immediately after extraction from the row
        lake_name_input = row[0].strip()
        ats_input = row[1].strip()
        lake_name_other_input = row[2].strip() 
        
        # --- Start Database Lookup Logic ---
        possible_lakes = Lake.objects.filter(Q(ats=ats_input))
        num_lakes = len(possible_lakes)
        matched_lake = None 

        if num_lakes == 0:
            print (f"none found for ATS: {ats_input}")

        elif num_lakes == 1:
            # If only one lake is found by ATS, it is the match.
            matched_lake = possible_lakes.first()
            # print (f'Lake found uniquely by ATS: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}')

        elif num_lakes > 1:
            print(f'Looking for: {lake_name_input} {lake_name_other_input} / {ats_input}')
            print (f'Multiple lakes found by ATS ({num_lakes} results). Attempting match by Name logic...')
            
            for lake in possible_lakes:
                
                # Clean the database values once for this loop iteration
                db_name = lake.name.strip().lower()
                db_other_name = lake.other_name.strip().lower()
                
                # Print clean values for debugging
                print (f'Possible lake: {db_name} {db_other_name} {lake.ats.strip()}')
                
                # Condition A: Check for a perfect match on both name fields (Most reliable)
                is_full_match = (db_name == lake_name_input.lower()) and \
                                (db_other_name == lake_name_other_input.lower())
                
                # Condition B: Check for the "Unnamed" transfer logic
                # The database's main name is a placeholder AND the database's other_name matches the input's main name
                is_transfer_match = (db_name =="unnamed") and \
                                    (db_other_name == lake_name_input.lower())
                
                # Combine the conditions
                if is_full_match or is_transfer_match:
                    matched_lake = lake 
                    print(f'*** SUCCESS: Matched lake using Full Match OR Unnamed Transfer Logic! ***')
                    break  
                
            print ("=================")

            if matched_lake:
                print (f'Final Lake found: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}')
            else:
                print (f'No unique lake found using name criteria among the multiples for ATS {ats_input}.')





FILE_NAME = 'extra files/epa-alberta-fish-stocking-report-2025.csv'

def run():
    df = get_data (FILE_NAME)
    # print(df.head())
    check_lakes_with_name_transfer_logic (df)