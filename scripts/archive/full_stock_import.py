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
    
    # Apply full cleaning (including the necessary \n removal) and create CLEAN columns
    df['Input_Name_Clean'] = df['Col0'].astype(str).str.replace('\n', ' ', regex=False).str.strip().str.lower().replace('nan', '')
    df['Input_Other_Name_Clean'] = df['Col1'].astype(str).str.replace('\n', ' ', regex=False).str.strip().str.lower().replace('nan', '')
    df['Input_ATS'] = df['Col2'].astype(str).str.strip().str.upper().replace('nan', '')

    # Identify unique lake entries using the CLEAN columns
    # NOTE: The original code had a KeyError here. Using the CLEAN columns fixes it.
    unique_lakes = df[['Input_Name_Clean', 'Input_Other_Name_Clean', 'Input_ATS']].drop_duplicates().reset_index(drop=True)

    # Track lakes that couldn't be uniquely matched to suggest for database additions
    unmatched_lakes = []

    for index, row in unique_lakes.iterrows():
        # Use the CLEANED names consistently from the unique_lakes DataFrame
        ats_input = row['Input_ATS']
        lake_name_input_clean = row['Input_Name_Clean']
        lake_name_other_input_clean = row['Input_Other_Name_Clean']
        
        # Skip records missing essential identifying data
        if not ats_input or (not lake_name_input_clean and not lake_name_other_input_clean):
            # Using the cleaned names for printing consistency
            print(f"Skipping incomplete record: Name='{lake_name_input_clean}', Other='{lake_name_other_input_clean}', ATS='{ats_input}'")
            continue

        # 1. Primary Match: Find all existing lakes in the database with this ATS
        lakes_with_matching_ats = Lake.objects.filter(Q(ats__iexact=ats_input))
        
        num_matches = lakes_with_matching_ats.count()
        matched_lake = None
        ambiguous_match = False

        if num_matches == 0:
            # Case 3: No ATS match - suggest adding a new lake
            print(f"FAIL: No lake found in DB for ATS '{ats_input}'. Suggest adding: Name='{lake_name_input_clean}', Other='{lake_name_other_input_clean}'.")
            unmatched_lakes.append(row)
            continue
            
        elif num_matches == 1:
            # Case 1: Perfect ATS match (the '95% works great' scenario)
            matched_lake = lakes_with_matching_ats.first()
            # If you want to see the 95% successes, uncomment the next line:
            # print(f"SUCCESS (ATS only): Matched DB Lake: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}")
            
        else:
            # Case 2: Multiple ATS matches - requires name-matching logic
            print(f"INFO: Multiple lakes ({num_matches}) found for ATS '{ats_input}'. Applying name logic...")
            
            # THE LOGIC LOOP AND RESULT CHECK MUST BE INSIDE THIS ELSE BLOCK
            for lake in lakes_with_matching_ats:
                db_name = lake.name.strip().lower()
                db_other_name = lake.other_name.strip().lower()

                # Rule 1: Full Match (Main and Other name match)
                is_full_match = (db_name == lake_name_input_clean) and \
                                (db_other_name == lake_name_other_input_clean)

                # Rule 2: 'Unnamed' Transfer Logic (Original, where DB name is Unnamed)
                # Matches if DB main name is "unnamed" AND DB other name matches input's MAIN name (unlikely for "unnamed" input records)
                is_transfer_match_original = (db_name == "unnamed") and \
                                            (db_other_name == lake_name_input_clean)

                # Rule 3: Corrected Rule for "Unnamed" INPUT data (Fixes SE24-21-11-W5)
                # Matches if Input Main Name is "unnamed" AND Input Other Name matches DB main or other name
                is_unnamed_input_match = (lake_name_input_clean == "unnamed") and \
                                         (db_name == lake_name_other_input_clean or db_other_name == lake_name_other_input_clean)
                
                # Combine all conditions
                if is_full_match or is_transfer_match_original or is_unnamed_input_match:
                    if matched_lake is None:
                        matched_lake = lake
                    else:
                        # Ambiguous match found
                        matched_lake = 'AMBIGUOUS' 
                        ambiguous_match = True
                        break # Stop checking for this ATS once ambiguity is confirmed
            
            # Final check after the name logic loop (Only runs if num_matches > 1)
            if ambiguous_match:
                print(f"FAIL: AMBIGUOUS name match for '{lake_name_input_clean}' ({ats_input}). Manual resolution needed.")
                unmatched_lakes.append(row)
            elif matched_lake:
                # A unique name match was found
                print(f"*** SUCCESS (Name Logic): Matched DB Lake: {matched_lake.name.strip()} {matched_lake.other_name.strip()} {matched_lake.ats.strip()}")
            else:
                # No unique name match was found among the multiple ATS matches
                print (f'FAIL: No unique lake found using name criteria among the multiples for ATS {ats_input}. Manual resolution needed.')
                unmatched_lakes.append(row)

    print("\n--- Lake Matching Complete ---")
    return unmatched_lakes


# Add the standard entry point for Django runscript
# FILE_NAME = 'extra files/epa-alberta-fish-stocking-report-2025.csv'
FILE_NAME = 'extra files/test.csv'
# FILE_NAME = 'extra files/stocks_final_cleaned.csv'

def run():
    # Placeholder for get_data, assuming it reads the CSV into a DataFrame
    # In a real Django environment, you'd load the data here.
    try:
        df = pd.read_csv(FILE_NAME, header=None, skiprows=1)
    except FileNotFoundError:
        # Assuming the file is accessible since you are running it
        df = pd.read_csv(FILE_NAME, header=None, skiprows=1)

    unmatched_lakes = check_lakes_with_name_transfer_logic (df)

    print(f"Lakes requiring potential new database entry or manual action: {len(unmatched_lakes)}")

    