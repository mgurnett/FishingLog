import os # To manage file paths
import re
import csv
from datetime import datetime
import pandas as pd
import tabula
from django.db.models import Q
from catches.models import *

# --- Configuration ---
PDF_PATH = "scripts/fp-alberta-fish-stocking-report-2026.pdf" 
CSV_FILENAME = "scripts/csv_data.csv"


# Official Column Names based on PDF structure
COL_NAMES = [
    'Lake_Name',           
    'Common_Name',         
    'ATS_Location',        
    'Species_Code',        
    'Strain',       
    'Genotype',     
    'Avg_Length',       
    'Quantity_Stocked',    
    'Stocking_Date'  ]

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
    ('Trout Lodge / Silvers', 'TLTLS'),
    ("Trout Lodge/Silver's", 'TLTLS'),
    ('Bow River', 'BRBE'),
    ('Beitty/Bow River', 'BRBE'),
    ('Lac Ste. Anne', 'LSE'),
    ('Job Lake', 'JBL'),
    ('Allison Creek', "AC"),
    ('Riverence', "RD"),
    ('Marie Creek', 'MC'),
    ('Rock Island', 'RI'),]

SPECIES_CODES = ["RNTR", "CTTR", "WSCT", "WALL", "BKTR", "BNTR", "TGTR"]

GENOTYPE_CODES = ["2N", "3N", "AF2N", "AF3N"]

#regex patterns
ATS_PATTERN = r'^[NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-W\d{1}$'
SIMPLE_ATS_PATTERN = r'([NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
AVG_LENGTH_PATTERN = r'(\d{1,3}[.,]\d{1,2})'
# Quantity Pattern: Targets the large number with optional commas
QTY_PATTERN = r'(\d{1,3}(?:,\d{3})*)'
# Date Pattern (D-Mon-YY format)
DATE_PATTERN = r'(\d{1,2}\s*[\-\/]\s*[A-Za-z]{3}\s*[\-\/]\s*\d{2,4})'


# ================ STEP 1 Get table from PDF ==============================================================
def extract_and_save_tables():
    
    # 1. Extraction: Get the list of DataFrames
    # Use 'all' for all pages and 'stream' for better table recognition (default is 'lattice')
    try:
        list_of_dfs = tabula.read_pdf(
            PDF_PATH, 
            pages='all',
            output_format='dataframe',
            # Add other options here, like area='...', guess=False, etc.
        )
    except Exception as e:
        message = (f"An error occurred during PDF extraction: {e}")
        return

    if not list_of_dfs:
        message = ("No tables were extracted. Check your PDF and extraction parameters.")
        return

    message = (f"Successfully extracted {len(list_of_dfs)} table(s).\n Saved all {len(list_of_dfs)} tables combined")
      
    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    
    # Save the combined DataFrame to a single CSV file
    return combined_df, message


# ================ STEP 2 clean up the data ==============================================================
def is_valid_ats_code(text):
    """
    Checks if a given string matches the required ATS location code pattern.
    """
    return bool(re.match(ATS_PATTERN, text))

def get_ats_cell_index(row: pd.Series):
    """
    Finds the index of the cell containing a valid ATS code.

    Args:
        row: A single row from a pandas DataFrame (pd.Series).

    Returns:
        The integer position of the cell (0-indexed) or None.
    """
    # 1. Convert to string and find matches
    string_series = row.astype(str)
    mask = string_series.str.match(ATS_PATTERN, na=False)
    
    # 2. Check if a match exists
    if mask.any():
        # Get the label (column name) of the first True match
        column_label = mask.idxmax() 
        
        # Return the integer position of that label
        return row.index.get_loc(column_label)
    
    return None

def validate_all_data(df):
        # 1. Rename columns and force to 'object' type to avoid TypeError/LossySetitemError
    df.columns = COL_NAMES
    df = df.astype(object)
    
    total_rows = len(df)
    df['row_type'] = ""
    df['ats_index'] = ""

    # --- Phase 1: Fix Alignment and Categorize ---
    for index in range(total_rows):
        current_row = df.iloc[index]
        ats_index = get_ats_cell_index(current_row)

        # Categorize the row
        if ats_index:
            df.at[index, 'row_type'] = "main"
            df.at[index, 'ats_index'] = str(ats_index)
        elif pd.notna(current_row.get('Strain')):
            df.at[index-1, 'row_type'] = "short"
            df.at[index, 'row_type'] = "strain"
        elif pd.notna(current_row.get('Species_Code')):
            df.at[index-1, 'row_type'] = "short"
            df.at[index, 'row_type'] = "species_code"
        else:
            df.at[index, 'row_type'] = "delete"

    # --- Phase 2: Merge and Filter ---
    # Drop "delete" rows and reset index for safe merging
    df = df[df['row_type'] != "delete"].copy().reset_index(drop=True)

    for row in range(len(df)):
        if df.at[row, 'row_type'] == "strain":
            first_part = df.at[row-1, 'Strain'].strip()
            second_part = df.at[row, 'Strain'].strip()
            df.at[row-1, 'Strain'] = f"{first_part} {second_part}".strip()
            df.at[row-1, 'row_type'] = "fixed"
            df.at[row, 'row_type'] = "delete"
        if df.at[row, 'row_type'] == "species_code":
            first_part = df.at[row-1, 'Species_Code'].strip()
            second_part = df.at[row, 'Species_Code'].strip()
            df.at[row-1, 'Species_Code'] = f"{first_part} {second_part}".strip()
            df.at[row-1, 'row_type'] = "fixed"
            df.at[row, 'row_type'] = "delete"

    df = df[df['row_type'] != "delete"].copy().reset_index(drop=True)

    for row in range(len(df)):
        if df.at[row, 'ats_index'] == 1:
            df.at[row, 'Strain'] = df.at[row, 'Species_Code']
            df.at[row, 'Species_Code'] = df.at[row, 'ATS_Location']
            df.at[row, 'ATS_Location'] = df.at[row, 'Common_Name']
            df.at[row, 'Common_Name'] = ""

    message = ("Success, the columns have been cleaned up")
    return df, message


# ================ STEP 3 clean up the data ==============================================================
def validate_and_clean_row(df):
    all_rows = [] 
    # Initialize the strain map for lookup
    strain_map = {name.lower(): code for name, code in STRAIN_lookup}

    for index, row in df.iterrows():
        row_dict = {k: "" for k in COL_NAMES}
        string_series = row.astype(str)
        
        # --- 1. Clean Lake Name ---
        if string_series['Lake_Name'] != "Unnamed" and string_series['Lake_Name'] != "nan":
            row_dict['Lake_Name'] = string_series['Lake_Name']
        else:
            row_dict['Lake_Name'] = string_series['Common_Name'] if string_series['Common_Name'] != "nan" else ""
        
        # --- 2. Robust ATS Location Extraction ---
        full_row_string = ' '.join(str(val) for val in string_series.values if pd.notna(val))
        
        try:
            full_row_series = pd.Series([full_row_string])
            extracted_ats = full_row_series.str.extract(SIMPLE_ATS_PATTERN, expand=False).iloc[0]
            
            if pd.isna(extracted_ats):
                row_dict['ATS_Location'] = "ATS_MISSING_ERROR" 
            else:
                row_dict['ATS_Location'] = extracted_ats.replace(' ', '').strip()
        except Exception as e:
            row_dict['ATS_Location'] = "ATS_EXTRACTION_ERROR"

        # --- 3. Validate and Extract Species Code ---
        pattern = '|'.join(SPECIES_CODES)
        species_val = string_series['Species_Code'].strip()
        
        try:
            is_species_present = any(code in species_val for code in SPECIES_CODES)
            row_dict['Species_Code'] = species_val if is_species_present else "Invalid"
        except:
            row_dict['Species_Code'] = "Not found" 

        # --- 4. Validate and Extract Genotype ---
        pattern_geno = '|'.join(GENOTYPE_CODES)
        genotype_val = string_series['Genotype'].strip()

        try:
            is_genotype_present = any(g.lower() in genotype_val.lower() for g in GENOTYPE_CODES)
            row_dict['Genotype'] = genotype_val.upper() if is_genotype_present else "Invalid"
        except:
            row_dict['Genotype'] = "Not found"   

        # --- 5. Strain Validation ---
        raw_strain = string_series['Strain'].strip()
        matched_code = strain_map.get(raw_strain.lower())
        
        if matched_code:
            row_dict['Strain'] = raw_strain
        else:
            found_partial = False
            for full_name, code in STRAIN_lookup:
                if full_name.lower() in raw_strain.lower() or raw_strain.lower() in full_name.lower():
                    row_dict['Strain'] = code
                    found_partial = True
                    break
            if not found_partial:
                row_dict['Strain'] = "Unknown Strain"

        # --- 6. Validate and Extract length ---
        try:
            extracted_length = pd.Series([full_row_string]).str.extract(AVG_LENGTH_PATTERN, expand=False).iloc[0]
            if pd.notna(extracted_length):
                cleaned_length_str = extracted_length.replace(',', '.')
                row_dict['Avg_Length'] = float(cleaned_length_str)
        except:
            pass

        # --- 7. Robust Quantity Stocked ---
        try:
            string_without_comma = string_series['Quantity_Stocked'].replace(',', '')
            row_dict['Quantity_Stocked'] = int(float(string_without_comma))
        except:
            row_dict['Quantity_Stocked'] = 0
        
        # --- 8. Robust Stocking Date Extraction ---
        try:
            extracted_date = pd.Series([full_row_string]).str.extract(DATE_PATTERN, expand=False).iloc[0]
            if pd.notna(extracted_date):
                date_time_obj = pd.to_datetime(extracted_date, errors='coerce')
                if pd.notna(date_time_obj):
                    row_dict['Stocking_Date'] = date_time_obj.strftime('%d-%m-%Y')
        except:
            pass

        all_rows.append(row_dict.copy()) 

    final_df = pd.DataFrame(all_rows)
    message = (f"Each row cleaned.")
    return final_df, message


# ================ STEP 4 each row cleaned up ==============================================================
def save_to_csv(df):
    df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
    message = (f"Success: All data has been saved to {CSV_FILENAME}")
    return message


# ================ STEP 5 check to see if all alkes are accounted for ======================================
def check_lakes_with_name_transfer_logic(df):
    """
    Identifies and matches unique lake entries in the fish stocking report (df)
    to existing Lake entries in the database using ATS, and then name-matching
    logic for multiple ATS record scenarios.

    This function relies o n the catches.models.Lake and django.db.models.Q objects.
    It performs a diagnostic check and prints the matching result or required action.
    """
    # print("--- Starting Lake Identification and Matching Logic ---")
    
    # Assuming CSV columns based on the 'epa-alberta-fish-stocking-report-2026.csv' structure:
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

    if unmatched_lakes:
        return df, "", unmatched_lakes
    else:
        return df, "All lakes checked successfully", unmatched_lakes


# ================ STEP 6 data is good, now delete the old.=================================================
def out_with_the_old(year_to_delete):
    Stock.objects.filter(date_stocked__year=year_to_delete).delete()
    message = f"All stocks from {year_to_delete} have been removed"
    return message

# ================ STEP 7 push cleaned up data to the database ===============================================
def stock_import_process(df):
    """
    Processes a cleaned DataFrame of stocking records, performs necessary lookups
    (Lake, Fish, Strain), and saves the Stock records to the database.
    """
    
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
        strain_to_find = str(row['Col4']).replace('\n', '').strip()
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

    message = (f'\n{total_trout_stocked:,} trout stocked\n{total_non_trout_stocked:,} non-trout stocked\nTotal of {total_fish_stocked:,}')
    return message


# ==============================================================================
# 🚀 MAIN
# ==============================================================================
def run():
    YEAR_TO_DELETE = 2026

# ================ STEP 1 Get table from PDF ==============================================================
    print(f"Attempting to extract tables from: {PDF_PATH}")
    initial_df, message = extract_and_save_tables()
    print(f"STEP 1: {message}")

# ================ STEP 2 clean up the data ==============================================================
    cleanedup_df, message = validate_all_data (initial_df)
    print(f"STEP 2: {message}")

# ================ STEP 3 clean up the data ==============================================================
    final_df,message = validate_and_clean_row (cleanedup_df)
    print(f"STEP 3: {message}")

# ================ STEP 4 each row cleaned up ==============================================================
    message = save_to_csv (final_df)
    print(f"STEP 4: {message}")

# ================ STEP 5 check to see if all lakes are accounted for ======================================
    checked_df, message, unmatched_lakes = check_lakes_with_name_transfer_logic(final_df)
    
    if unmatched_lakes:
        print(f"\n🛑 STOPPING: {len(unmatched_lakes)} lakes were not found or are ambiguous.")
        print("Please resolve these in the database before running again.")
        # Returning here stops the execution of STEP 6 and STEP 7
        return 
    else:
        print(f"STEP 5: {message}")

# ================ STEP 6 data is good, now delete the old.=================================================
    message = out_with_the_old(YEAR_TO_DELETE)
    print(f"STEP 6: {message}")

# ================ STEP 7 push cleaned up data to the database ===============================================
    message = stock_import_process(checked_df)
    print(f"STEP 7: {message}")


    print("--- Stock Record Import Complete ---")
    