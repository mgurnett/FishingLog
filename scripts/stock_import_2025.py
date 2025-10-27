from catches.models import *
import re
from datetime import datetime
import csv
import pandas as pd
from django.db.models import Q


# NOTE: I am assuming your Lake model and Q object are correctly imported and functional
# The full data cleaning (including the necessary \n removal) is now inside the function.

STRAIN_lookup = [\
    ('Beitty x Beitty', 'BEBE'),\
    ('Beitty Resort', 'BEBE'),\
    ('Bow River x Beitty', 'BRBE'),\
    ('Campbell Lake', 'CLCL'),\
    ('Lyndon', 'LYLY'),\
    ('Pit Lake', 'PLPL'),\
    ('Pit Lakes', 'PLPL'),\
    ('Trout Lodge / Jumpers', 'TLTLJ'),\
    ('Trout Lodge/Jumpers', 'TLTLJ'),\
    ('Trout Lodge / Kamloops', 'TLTLK'),\
    ('Trout Lodge/Kamloops', 'TLTLK'),\
    ('Trout Lodge/Kamloops', 'TLTLK'),\
    ('Trout Lodge / Silvers', 'TLTLS'),\
    ("Trout Lodge/Silver's", 'TLTLS'),\
    ('Bow River', 'BRBE'),\
    ('Beitty/Bow River', 'BRBE'),\
    ('Lac Ste. Anne', 'LSE'),\
    ('Job Lake', 'JBL'),\
    ('Allison Creek', "AC"),\
    ('Riverence', "RD"),\
    ('Marie Creek', 'MC'),\
    ('Rock Island', 'RI'),\
    ('Ethel Lake', 'EL'),\
    ('Graham Lake', 'GL'),\
 ]

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
                is_transfer_match_original = (db_name == "unnamed") and \
                                            (db_other_name == lake_name_input_clean)

                # Rule 3: Corrected Rule for "Unnamed" INPUT data (Fixes SE24-21-11-W5)
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
    print(f"Lakes requiring potential new database entry or manual action: {len(unmatched_lakes)}")
    
    # Return the fully cleaned and named DataFrame for the next processing stage
    return df


def stock_import_process(df):
    """
    Processes a cleaned DataFrame of stocking records, performs necessary lookups
    (Lake, Fish, Strain), and saves the Stock records to the database.
    """
    print("\n--- Starting Stock Record Import ---")
    
    # We assume df has already been cleaned and formatted by check_lakes_with_name_transfer_logic
    # Column mapping based on the provided logic:
    # Col0: Main Lake Name | Col1: Other Lake Name | Col2: ATS
    # Col3: Fish Abbrev    | Col4: Strain Name     | Col5: Genotype
    # Col6: Length         | Col7: Number          | Col8: Date
    
    # Initialize counters
    total_trout_stocked = 0
    total_non_trout_stocked = 0
    total_fish_stocked = 0
    
    num_lines = len(df)
    
    # Iterate over every row in the DataFrame for stocking
    for line_count, row in df.iterrows():
        # Reset matched objects for the new row
        lake_id = None
        fish_id = None
        strain = ""
        geo = ""
        date_object = None
        
        # --- 1. Lake Lookup (Same logic as phase 1, but for every row) ---
        ats_input = row['Input_ATS']
        lake_name_input_clean = row['Input_Name_Clean']
        lake_name_other_input_clean = row['Input_Other_Name_Clean']

        try:
            lakes_with_matching_ats = Lake.objects.filter(Q(ats__iexact=ats_input))
            
            if lakes_with_matching_ats.count() == 1:
                lake_id = lakes_with_matching_ats.first()
            elif lakes_with_matching_ats.count() > 1:
                # Apply name logic for ambiguity resolution
                matched_lake = None
                for lake in lakes_with_matching_ats:
                    db_name = lake.name.strip().lower()
                    db_other_name = lake.other_name.strip().lower()

                    is_full_match = (db_name == lake_name_input_clean) and (db_other_name == lake_name_other_input_clean)
                    is_unnamed_input_match = (lake_name_input_clean == "unnamed") and \
                                             (db_name == lake_name_other_input_clean or db_other_name == lake_name_other_input_clean)
                    
                    if is_full_match or is_unnamed_input_match:
                        if matched_lake is None:
                            matched_lake = lake
                        else:
                            # Ambiguous match found, skip this record for stocking
                            matched_lake = 'AMBIGUOUS'
                            break
                
                if isinstance(matched_lake, Lake):
                    lake_id = matched_lake
                else:
                    print(f'\nLAKE missing (Ambiguous/No Name Match): {row["Col0"]} ({row["Col1"]} ATS: {ats_input})')
                    continue # Skip to the next stock record
            else:
                print(f'\nLAKE missing (No ATS Match): {row["Col0"]} ({row["Col1"]} ATS: {ats_input})')
                continue # Skip to the next stock record
        except Exception as e:
            print(f'\nLAKE lookup error: {row["Col0"]} ({row["Col1"]} ATS: {ats_input}). Error: {e}')
            continue # Skip to the next stock record

        
        # --- 2. Fish Lookup ---
        try:
            fish_abbrev = str(row['Col3']).strip()
            fish_id = Fish.objects.get(abbreviation=fish_abbrev)
            
            # Count the stock amount (Col7)
            stock_number = int(row['Col7'])
            if fish_id.id in [7, 8, 9, 10, 14]:
                total_non_trout_stocked += stock_number
            else:
                total_trout_stocked += stock_number

        except Fish.DoesNotExist:
            print(f'\nFISH missing: {row["Col3"]} from Lake: {row["Col0"]} ({row["Col1"]})')
            continue # Skip to the next stock record
        except Exception:
            print(f'\nFISH missing (General Error): {row["Col3"]} from Lake: {row["Col0"]} ({row["Col1"]})')
            continue # Skip to the next stock record

        
        # --- 3. Strain Lookup ---
        found = 0
        strain_to_find = str(row['Col4']).replace('\n', ' ')
        for index, str_look in enumerate(STRAIN_lookup):
            if strain_to_find == str_look[0]:
                found = index
                break
        
        if found == 0:
            print(f'\nSTRAIN missing: {strain_to_find} from Lake: {row["Col0"]} ({row["Col1"]})')
            # You might want to continue here if a missing strain is a dealbreaker
            # For now, we will use an empty string for strain if not found
            strain = ""
        else:
            strain = STRAIN_lookup[found][1]

        
        # --- 4. Genotype ---
        if str(row['Col5']) in ("2N", "3N", "AF2N", "AF3N"):
            geo = str(row['Col5'])
        else:
            geo = ""

        
        # --- 5. Date Convert ---
        try:
            # Assuming row['Col8'] is a string date like 'DD-MM-YYYY'
            date_object = datetime.strptime(str(row['Col8']).strip(), '%d-%m-%Y').date()
        except ValueError:
            print(f'\nDate format incorrect for: {row["Col8"]}. Skipping record.')
            continue # Skip to the next stock record

        
        # --- 6. Save Stock Record ---
        try:
            stock = Stock(
                date_stocked = date_object, 
                number = stock_number,
                length = row['Col6'],
                lake = lake_id,
                fish = fish_id,
                strain = strain,
                gentotype = geo,
            )
            total_fish_stocked += stock_number
            stock.save()
        except Exception as e:
            print(f'\nError saving stock record for {row["Col0"]} ({row["Col1"]}). Error: {e}')


        # --- 7. Progress Update ---
        percent = round((line_count + 1) / num_lines * 100, 1)
        print (f'Line count: {line_count+1} of {num_lines} or {percent}% | {total_trout_stocked:,} trout stocked and {total_non_trout_stocked:,} non-trout stocked', end="\r")

    print(f'\n{total_trout_stocked:,} trout stocked and {total_non_trout_stocked:,} non-trout stocked for a total of {total_fish_stocked:,}')
    print("--- Stock Record Import Complete ---")


# Add the standard entry point for Django runscript
# FILE_NAME = 'extra files/epa-alberta-fish-stocking-report-2025.csv'
FILE_NAME = 'extra files/test.csv'

def run():

    print ("Deleting all stocks from 2025")
    Stock.objects.filter(date_stocked__year=2025).delete()
    print ("Done")

    # Placeholder for get_data, assuming it reads the CSV into a DataFrame
    try:
        # Load the raw DataFrame
        df = pd.read_csv(FILE_NAME, header=None, skiprows=1)
    except FileNotFoundError:
        # Assuming the file is accessible since you are running it
        df = pd.read_csv('epa-alberta-fish-stocking-report-2025.csv', header=None, skiprows=1)

    # 1. Run Diagnostic Check (and get the cleaned DataFrame back)
    df_cleaned = check_lakes_with_name_transfer_logic (df)
    
    # 2. Run the actual stock import using the cleaned DataFrame
    stock_import_process(df_cleaned)