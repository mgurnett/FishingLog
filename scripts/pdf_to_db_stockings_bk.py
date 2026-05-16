import os  # To manage file paths
import sys
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
CSV_FILENAME_debug = "scripts/csv_data_debug.csv"

# Official Column Names based on PDF structure
COL_NAMES = [
    'Lake_Name',           
    'ATS_Location',        
    'Species_Code',        
    'Strain',       
    'Genotype',     
    'Avg_Length',       
    'Quantity_Stocked',    
    'Stocking_Date'  
]

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
    ('Rock Island', 'RI'),
]

SPECIES_CODES = ["RNTR", "CTTR", "WSCT", "WALL", "BKTR", "BNTR", "TGTR"]
GENOTYPE_CODES = ["2N", "3N", "AF2N", "AF3N"]

# Regex patterns
ATS_PATTERN = r'^[NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-W\d{1}$'
# SIMPLE_ATS_PATTERN = r'([NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
SIMPLE_ATS_PATTERN = r'(?:[NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
AVG_LENGTH_PATTERN = r'(\d{1,3}[.,]\d{1,2})'
QTY_PATTERN = r'(\d{1,3}(?:,\d{3})*)'
DATE_PATTERN = r'(\d{1,2}\s*[\-\/]\s*[A-Za-z]{3}\s*[\-\/]\s*\d{2,4})'


# ================ STEP 1 Get table from PDF ==============================================================
def extract_and_save_tables():
    try:
        list_of_dfs = tabula.read_pdf(
            PDF_PATH, 
            pages='all',
            output_format='dataframe',
            stream=True  # Switched to stream for cleaner column grouping
        )
    except Exception as e:
        message = f"An error occurred during PDF extraction: {e}"
        return None, message

    if not list_of_dfs:
        message = "No tables were extracted. Check your PDF and extraction parameters."
        return None, message

    message = f"Successfully extracted {len(list_of_dfs)} table(s)."
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    return combined_df, message


# ================ STEP 2 clean up the data ==============================================================
def get_ats_cell_index(row: pd.Series):
    string_series = row.astype(str)
    mask = string_series.str.contains(SIMPLE_ATS_PATTERN, na=False, regex=True)
    if mask.any():
        column_label = mask.idxmax() 
        return row.index.get_loc(column_label)
    return None


def validate_all_data(df):
    if len(df.columns) != len(COL_NAMES):
        # Fallback handling if an extra/fewer columns extracted before processing
        df = df.iloc[:, :len(COL_NAMES)]
    
    df.columns = COL_NAMES
    df = df.astype(object)
    
    total_rows = len(df)
    df['row_type'] = ""
    df['ats_index'] = ""

    # --- Phase 1: Fix Alignment, Split Merged Columns, and Categorize ---
    for index in range(total_rows):
        current_row = df.iloc[index]
        ats_index = get_ats_cell_index(current_row)

        if ats_index == 0:
            full_text = str(current_row.iloc[0])
            ats_match = re.search(SIMPLE_ATS_PATTERN, full_text)
            if ats_match:
                actual_ats = ats_match.group(0)
                lake_name = full_text.replace(actual_ats, "").strip()
                
                df.at[index, 'Lake_Name'] = lake_name
                df.at[index, 'ATS_Location'] = actual_ats
                df.at[index, 'row_type'] = "main"
                df.at[index, 'ats_index'] = "1"
        
        elif ats_index:
            df.at[index, 'row_type'] = "main"
            df.at[index, 'ats_index'] = str(ats_index)
        
        elif pd.notna(current_row.get('Strain')) and str(current_row.get('Strain')) != 'nan':
            df.at[index-1, 'row_type'] = "short"
            df.at[index, 'row_type'] = "strain"
        
        elif pd.notna(current_row.get('Species_Code')) and str(current_row.get('Species_Code')) != 'nan':
            df.at[index-1, 'row_type'] = "short"
            df.at[index, 'row_type'] = "species_code"
        
        else:
            df.at[index, 'row_type'] = "delete"

    # --- Phase 2: Merge and Filter ---
    df = df[df['row_type'] != "delete"].copy().reset_index(drop=True)

    for row in range(len(df)):
        if df.at[row, 'row_type'] == "strain":
            first_part = str(df.at[row-1, 'Strain']).strip()
            second_part = str(df.at[row, 'Strain']).strip()
            if first_part == 'nan': first_part = ""
            if second_part == 'nan': second_part = ""
            df.at[row-1, 'Strain'] = f"{first_part} {second_part}".strip()
            df.at[row-1, 'row_type'] = "fixed"
            df.at[row, 'row_type'] = "delete"
            
        if df.at[row, 'row_type'] == "species_code":
            first_part = str(df.at[row-1, 'Species_Code']).strip()
            second_part = str(df.at[row, 'Species_Code']).strip()
            if first_part == 'nan': first_part = ""
            if second_part == 'nan': second_part = ""
            df.at[row-1, 'Species_Code'] = f"{first_part} {second_part}".strip()
            df.at[row-1, 'row_type'] = "fixed"
            df.at[row, 'row_type'] = "delete"

    df = df[df['row_type'] != "delete"].copy().reset_index(drop=True)

    # Clean shifted indexes securely without 'Common_Name' reference dependencies
    for row in range(len(df)):
        if df.at[row, 'ats_index'] == '1' and df.at[row, 'row_type'] == 'main' and pd.isna(df.at[row, 'Stocking_Date']):
             pass 

    message = "Success, the columns have been cleaned up"
    df.to_csv(CSV_FILENAME_debug, index=False, encoding='utf-8')
    return df, message


# ================ STEP 3 clean up the data ==============================================================
def validate_and_clean_row(df):
    all_rows = [] 
    strain_map = {name.lower(): code for name, code in STRAIN_lookup}

    for index, row in df.iterrows():
        row_dict = {k: "" for k in COL_NAMES}
        string_series = row.astype(str)
        
        # --- 1. Clean Lake Name ---
        lake_val = string_series['Lake_Name'].strip()
        row_dict['Lake_Name'] = lake_val if lake_val not in ["Unnamed", "nan"] else "Unnamed"
        
        # --- 2. Robust ATS Location Extraction ---
        full_row_string = ' '.join(str(val) for val in string_series.values if pd.notna(val))
        try:
            full_row_series = pd.Series([full_row_string])
            extracted_ats = full_row_series.str.extract(SIMPLE_ATS_PATTERN, expand=False).iloc[0]
            row_dict['ATS_Location'] = "ATS_MISSING_ERROR" if pd.isna(extracted_ats) else extracted_ats.replace(' ', '').strip()
        except:
            row_dict['ATS_Location'] = "ATS_EXTRACTION_ERROR"

        # --- 3. Validate and Extract Species Code ---
        species_val = string_series['Species_Code'].strip()
        is_species_present = any(code in species_val for code in SPECIES_CODES)
        row_dict['Species_Code'] = species_val if is_species_present else "Invalid"

        # --- 4. Validate and Extract Genotype ---
        genotype_val = string_series['Genotype'].strip()
        is_genotype_present = any(g.lower() in genotype_val.lower() for g in GENOTYPE_CODES)
        row_dict['Genotype'] = genotype_val.upper() if is_genotype_present else "Invalid"

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
                row_dict['Avg_Length'] = float(extracted_length.replace(',', '.'))
        except:
            row_dict['Avg_Length'] = 0.0

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
            row_dict['Stocking_Date'] = ""

        all_rows.append(row_dict.copy()) 

    final_df = pd.DataFrame(all_rows)
    return final_df, "Each row cleaned."


# ================ STEP 4 each row cleaned up ==============================================================
def save_to_csv(df):
    df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
    return f"Success: All data has been saved to {CSV_FILENAME}"


# ================ STEP 5 check to see if all lakes are accounted for ======================================
def check_lakes_with_name_transfer_logic(df):
    # Retain explicit namespaces from Step 3 cleanly instead of using numeric assignments
    df['Input_Name_Clean'] = df['Lake_Name'].astype(str).str.replace('\n', ' ', regex=False).str.strip().str.lower().replace('nan', '')
    df['Input_ATS'] = df['ATS_Location'].astype(str).str.strip().str.upper().replace('nan', '')

    unique_lakes = df[['Input_Name_Clean', 'Input_ATS']].drop_duplicates().reset_index(drop=True)
    unmatched_lakes = []

    for index, row in unique_lakes.iterrows():
        ats_input = row['Input_ATS']
        lake_name_input_clean = row['Input_Name_Clean']
        
        if not ats_input or ats_input == "ATS_MISSING_ERROR":
            continue

        lakes_with_matching_ats = Lake.objects.filter(Q(ats__iexact=ats_input))
        num_matches = lakes_with_matching_ats.count()

        if num_matches == 0:
            print(f"FAIL: No lake found in DB for ATS '{ats_input}'. Name='{lake_name_input_clean}'")
            unmatched_lakes.append(row)
            continue
            
        elif num_matches > 1:
            matched_lake = None
            for lake in lakes_with_matching_ats:
                db_name = lake.name.strip().lower()
                if db_name == lake_name_input_clean or db_name == "unnamed":
                    matched_lake = lake
                    break
            if not matched_lake:
                unmatched_lakes.append(row)

    if unmatched_lakes:
        return df, "", unmatched_lakes
    return df, "All lakes checked successfully", unmatched_lakes


# ================ STEP 6 data is good, now delete the old.=================================================
def out_with_the_old(year_to_delete):
    Stock.objects.filter(date_stocked__year=year_to_delete).delete()
    return f"All stocks from {year_to_delete} have been removed"


# ================ STEP 7 push cleaned up data to the database ===============================================
def stock_import_process(df):
    total_trout_stocked = 0
    total_non_trout_stocked = 0
    total_fish_stocked = 0
    num_lines = len(df)
    
    for line_count, row in df.iterrows():
        ats_input = row['ATS_Location']
        lake_name_input_clean = str(row['Lake_Name']).strip().lower()

        try:
            lakes_with_matching_ats = Lake.objects.filter(Q(ats__iexact=ats_input))
            if lakes_with_matching_ats.count() == 1:
                lake_id = lakes_with_matching_ats.first()
            elif lakes_with_matching_ats.count() > 1:
                matched_lake = None
                for lake in lakes_with_matching_ats:
                    if lake.name.strip().lower() == lake_name_input_clean or lake.name.strip().lower() == "unnamed":
                        matched_lake = lake
                        break
                lake_id = matched_lake
            else:
                continue
        except:
            continue

        if not lake_id:
            continue

        # Fish Lookup
        try:
            fish_abbrev = str(row['Species_Code']).strip()
            fish_id = Fish.objects.get(abbreviation=fish_abbrev)
            stock_number = int(row['Quantity_Stocked'])
            
            if fish_id.id in [7, 8, 9, 10, 14]:
                total_non_trout_stocked += stock_number
            else:
                total_trout_stocked += stock_number
        except:
            continue

        # Strain Validation
        strain_to_find = str(row['Strain']).strip()
        strain = ""
        for str_look in STRAIN_lookup:
            if strain_to_find == str_look[0] or strain_to_find == str_look[1]:
                strain = str_look[1]
                break
        
        geo = str(row['Genotype']) if str(row['Genotype']) in ("2N", "3N", "AF2N", "AF3N") else ""

        # Date Format Normalization Check
        try:
            date_object = datetime.strptime(str(row['Stocking_Date']).strip(), '%d-%m-%Y').date()
        except:
            continue

        # Save Entry Securely
        try:
            stock = Stock(
                date_stocked=date_object, 
                number=stock_number,
                length=row['Avg_Length'],
                lake=lake_id,
                fish=fish_id,
                strain=strain,
                gentotype=geo,
            )
            total_fish_stocked += stock_number
            stock.save()
        except Exception as e:
            print(f'Saving row execution failure: {e}')

        percent = round((line_count + 1) / num_lines * 100, 1)
        print(f'Line count: {line_count+1} of {num_lines} or {percent}% | {total_trout_stocked:,} trout stocked', end="\r")

    return f'\n{total_trout_stocked:,} trout stocked\nTotal of {total_fish_stocked:,} database writes complete.'


# ==============================================================================
# 🚀 MAIN
# ==============================================================================
def run():
    YEAR_TO_DELETE = 2026

    print(f"Attempting to extract tables from: {PDF_PATH}")
    initial_df, message = extract_and_save_tables()
    print(f"STEP 1: {message}")
    if initial_df is None:
        sys.exit(1)  

    cleanedup_df, message = validate_all_data(initial_df)
    print(f"STEP 2: {message}")

    final_df, message = validate_and_clean_row(cleanedup_df)
    print(f"STEP 3: {message}")

    message = save_to_csv(final_df)
    print(f"STEP 4: {message}")

    checked_df, message, unmatched_lakes = check_lakes_with_name_transfer_logic(final_df)
    
    if unmatched_lakes:
        print(f"\n🛑 STOPPING: {len(unmatched_lakes)} lakes were not found or are ambiguous.")
        print("Please resolve these in the database before running again.")
        return 
    else:
        print(f"STEP 5: {message}")

    # Uncomment these when ready to write data 
    # message = out_with_the_old(YEAR_TO_DELETE)
    # print(f"STEP 6: {message}")

    # message = stock_import_process(checked_df)
    # print(f"STEP 7: {message}")

    print("--- Stock Record Import Complete ---")