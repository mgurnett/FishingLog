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

'''
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
            # print (f"none found for ATS: {ats_input}")
            pass

        elif num_lakes == 1:
            # If only one lake is found by ATS, it is the match.
            matched_lake = possible_lakes.first()
            # print (f'Lake found uniquely by ATS: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}')

        elif num_lakes > 1:
            # print(f'Looking for: {lake_name_input} {lake_name_other_input} / {ats_input}')
            # print (f'Multiple lakes found by ATS ({num_lakes} results). Attempting match by Name logic...')
            
            for lake in possible_lakes:
                
                # Clean the database values once for this loop iteration
                db_name = lake.name.strip().lower()
                db_other_name = lake.other_name.strip().lower()
                
                # Print clean values for debugging
                # print (f'Possible lake: {db_name} {db_other_name} {lake.ats.strip()}')
                
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
                
            # print ("=================")

            if matched_lake:
                # print (f'Final Lake found: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}')
                pass
            else:
                print (f'No unique lake found using name criteria among the multiples for ATS {ats_input}.')
'''

# import pandas as pd
# import re
# # Assuming the following imports are available in your Django project environment
# from catches.models import * from django.db.models import Q 

def check_lakes_with_name_transfer_logic(df):
    """
    Identifies and matches unique lake entries in the fish stocking report (df)
    to existing Lake entries in the database using ATS, and then name-matching
    logic for multiple ATS record scenarios.

    This function relies on the catches.models.Lake and django.db.models.Q objects.
    It performs a diagnostic check and prints the matching result or required action.
    """
    print("--- Starting Lake Identification and Matching Logic ---")
    
    # Assuming CSV columns based on the 'epa-alberta-fish-stocking-report-2025.csv' structure:
    # Column 0: Main Lake Name (Input_Name)
    # Column 1: Other Lake Name (Input_Other_Name)
    # Column 2: ATS (Input_ATS)
    df.columns = [f'Col{i}' for i in range(len(df.columns))]
    
    # Assuming you have already performed the full cleaning: 
    df['Input_Name_Clean'] = df['Col0'].str.replace('\n', ' ').str.strip().str.lower()
    df['Input_Other_Name_Clean'] = df['Col1'].str.replace('\n', ' ').str.strip().str.lower()
    df['Input_ATS'] = df['Col2'].astype(str).str.strip().str.upper().replace('nan', '')

    # Identify unique lake entries in the input CSV (one record per unique lake/ATS/other name combination)
    unique_lakes = df[['Input_Name', 'Input_Other_Name', 'Input_ATS']].drop_duplicates()

    # Track lakes that couldn't be uniquely matched to suggest for database additions
    unmatched_lakes = []

    for index, row in unique_lakes.iterrows():
        lake_name_input = row['Input_Name']
        lake_name_other_input = row['Input_Other_Name']
        ats_input = row['Input_ATS']
        
        # Skip records missing essential identifying data
        if not ats_input or (not lake_name_input and not lake_name_other_input):
            print(f"Skipping incomplete record: Name='{lake_name_input}', Other='{lake_name_other_input}', ATS='{ats_input}'")
            continue

        # 1. Primary Match: Find all existing lakes in the database with this ATS
        # Use Q object for case-insensitive ATS matching (as is common practice)
        lakes_with_matching_ats = Lake.objects.filter(Q(ats__iexact=ats_input))
        
        num_matches = lakes_with_matching_ats.count()
        matched_lake = None
        ambiguous_match = False

        if num_matches == 0:
            # Case 3: No ATS match - suggest adding a new lake
            print(f"FAIL: No lake found in DB for ATS '{ats_input}'. Suggest adding: Name='{lake_name_input}', Other='{lake_name_other_input}'.")
            unmatched_lakes.append(row)
            continue
            
        elif num_matches == 1:
            # Case 1: Perfect ATS match (the '95% works great' scenario)
            matched_lake = lakes_with_matching_ats.first()
            # print(f"SUCCESS (ATS only): Matched DB Lake: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}")
            
        else:
            # Case 2: Multiple ATS matches - requires name-matching logic
            print(f"INFO: Multiple lakes ({num_matches}) found for ATS '{ats_input}'. Applying name logic...")
            
            # This logic is based on your full_stock_import.py snippet and requirements 
            
        for lake in lakes_with_matching_ats:
            db_name = lake.name.strip().lower()
            db_other_name = lake.other_name.strip().lower()

            # Input variables are already cleaned (from the previous step's fix)
            lake_name_input = row['Input_Name_Clean']
            lake_name_other_input = row['Input_Other_Name_Clean']
            
            # Rule 1: Full Match (Main and Other name match)
            is_full_match = (db_name == lake_name_input) and \
                            (db_other_name == lake_name_other_input)

            # Rule 2: 'Unnamed' Transfer Logic (The original logic, which is likely for *other* data)
            # This checks if the DB's OTHER name matches the input's MAIN name.
            is_transfer_match_original = (db_name == "unnamed") and \
                                        (db_other_name == lake_name_input)

            # Rule 3 (NEW/CORRECTED RULE FOR THIS DATA): 
            # When Input Main Name is "unnamed," match the DB's main or other name 
            # against the Input Other Name. This is the crucial step.
            is_unnamed_input_match = (lake_name_input == "unnamed") and \
                                    (db_name == lake_name_other_input or db_other_name == lake_name_other_input)
            
            # Combine all conditions
            if is_full_match or is_transfer_match_original or is_unnamed_input_match:
                if matched_lake is None:
                    matched_lake = lake
                else:
                    # Ambiguous match found
                    matched_lake = 'AMBIGUOUS' 
                    ambiguous_match = True
                    break
            
            # Final check after the name logic loop
            if ambiguous_match:
                print(f"FAIL: AMBIGUOUS name match for '{lake_name_input}' ({ats_input}). Manual resolution needed.")
                unmatched_lakes.append(row)
            elif matched_lake:
                # A unique name match was found
                print(f"*** SUCCESS (Name Logic): Matched DB Lake: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}")
            else:
                # No name match was found among the multiple ATS matches
                print (f'FAIL: No unique lake found using name criteria among the multiples for ATS {ats_input}. Manual resolution needed.')
                unmatched_lakes.append(row)

    print("\n--- Lake Matching Complete ---")
    print(f"Lakes requiring potential new database entry or manual action: {len(unmatched_lakes)}")


FILE_NAME = 'extra files/epa-alberta-fish-stocking-report-2025.csv'

def run():
    df = get_data (FILE_NAME)
    # print(df.head())
    check_lakes_with_name_transfer_logic (df)