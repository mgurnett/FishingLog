import os
import sys
import re
import csv
from datetime import datetime as dt
import pandas as pd
import tabula
from django.db.models import Q
from catches.models import *

# --- File Paths & Configurations ---
PDF_PATH = "scripts/fp-alberta-fish-stocking-report-2026.pdf" 
CSV_FILENAME = "scripts/csv_data.csv"

# Official Target Column Names
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

# Master Non-Capturing Regular Expressions
SIMPLE_ATS_PATTERN = r'(?:[NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
AVG_LENGTH_PATTERN = r'(\d{1,3}[.,]\d{1,2})'
DATE_PATTERN = r'(\d{1,2}\s*[\-\/]\s*[A-Za-z]{3}\s*[\-\/]\s*\d{2,4})'


# ================ STREAM EXTRACTION ENGINE ==============================================================
def extract_pdf_to_raw_rows():
    """
    Extracts all pages from the PDF as dataframes using stream mode,
    then merges cell elements into clean tokenizable string streams.
    """
    try:
        dfs = tabula.read_pdf(PDF_PATH, pages='all', output_format='dataframe', stream=True)
    except Exception as e:
        print(f"🛑 Error loading file via Tabula: {e}")
        return []

    if not dfs:
        return []

    raw_text_rows = []
    for df in dfs:
        for _, row in df.iterrows():
            row_text = " ".join([str(val).strip() for val in row.values if pd.notna(val) and str(val).lower() != 'nan'])
            if row_text:
                raw_text_rows.append(row_text)
                
    return raw_text_rows


def parse_and_structure_rows(raw_rows):
    """
    Sifts through the text lines, isolates data using the ATS code as an anchor,
    and handles lines that wrapped down on the PDF table.
    """
    structured_records = []
    current_lake_name = "Unknown"
    current_ats = None

    for line in raw_rows:
        ats_match = re.search(SIMPLE_ATS_PATTERN, line)
        
        if ats_match:
            current_ats = ats_match.group(0).upper()
            line_parts = re.split(SIMPLE_ATS_PATTERN, line, maxsplit=1)
            left_side = line_parts[0].strip()
            right_side = line_parts[1].strip() if len(line_parts) > 1 else ""
            
            if left_side and left_side.lower() != "unnamed":
                current_lake_name = left_side
            elif not left_side:
                current_lake_name = "Unnamed"

            right_tokens = right_side.split()
            
            species = ""
            strain = ""
            genotype = ""
            length = "0.0"
            qty = "0"
            date = ""

            for token in right_tokens:
                if token.upper() in SPECIES_CODES:
                    species = token.upper()
                elif token.upper() in GENOTYPE_CODES:
                    genotype = token.upper()
                elif re.match(r'^\d{1,2}-[A-Za-z]{3}-\d{2,4}$', token):
                    date = token
                elif "." in token and token.replace('.', '', 1).isdigit():
                    length = token
                elif token.replace(',', '').isdigit():
                    qty = token.replace(',', '')
                else:
                    if token.lower() != "unnamed":
                        strain = f"{strain} {token}".strip()

            record = {
                'Lake_Name': current_lake_name,
                'ATS_Location': current_ats,
                'Species_Code': species,
                'Strain': strain if strain else "Unknown Strain",
                'Genotype': genotype if genotype else "2N",
                'Avg_Length': length,
                'Quantity_Stocked': qty,
                'Stocking_Date': date
            }
            structured_records.append(record)
            
        else:
            if not structured_records:
                continue
                
            last_record = structured_records[-1]
            tokens = line.split()
            
            if tokens and tokens[0].upper() in SPECIES_CODES:
                new_record = {
                    'Lake_Name': last_record['Lake_Name'],
                    'ATS_Location': last_record['ATS_Location'],
                    'Species_Code': tokens[0].upper(),
                    'Strain': "",
                    'Genotype': "",
                    'Avg_Length': "0.0",
                    'Quantity_Stocked': "0",
                    'Stocking_Date': ""
                }
                
                for token in tokens[1:]:
                    if token.upper() in GENOTYPE_CODES:
                        new_record['Genotype'] = token.upper()
                    elif re.match(r'^\d{1,2}-[A-Za-z]{3}-\d{2,4}$', token):
                        new_record['Stocking_Date'] = token
                    elif "." in token and token.replace('.', '', 1).isdigit():
                        new_record['Avg_Length'] = token
                    elif token.replace(',', '').isdigit():
                        new_record['Quantity_Stocked'] = token.replace(',', '')
                    else:
                        new_record['Strain'] = f"{new_record['Strain']} {token}".strip()
                        
                if not new_record['Strain']:
                    new_record['Strain'] = "Unknown Strain"
                structured_records.append(new_record)
            else:
                extra_text = " ".join(tokens)
                if "trout" not in extra_text.lower() and len(extra_text) > 2:
                    if last_record['Strain'] == "Unknown Strain":
                        last_record['Strain'] = extra_text
                    else:
                        last_record['Strain'] = f"{last_record['Strain']} {extra_text}".strip()

    return structured_records


# ================ STANDARDIZATION ENGINE ==============================================================
def standardize_and_clean_records(records):
    """
    Standardizes data formats, normalizing the strain names to the formal,
    fully written-out string versions from the lookup dictionary.
    """
    cleaned_records = []

    for rec in records:
        # Normalize and find the fully written out strain name
        raw_strain = rec['Strain'].strip()
        found_full_name = None

        for full_name, code in STRAIN_lookup:
            if (raw_strain.lower() == code.lower() or 
                raw_strain.lower() == full_name.lower() or 
                full_name.lower() in raw_strain.lower() or 
                raw_strain.lower() in full_name.lower()):
                found_full_name = full_name
                break

        if found_full_name:
            rec['Strain'] = found_full_name
        elif not raw_strain or raw_strain.lower() == "unknown strain":
            rec['Strain'] = "Unknown Strain"
        else:
            rec['Strain'] = raw_strain

        # Force numeric lengths and counts
        try:
            rec['Avg_Length'] = float(str(rec['Avg_Length']).replace(',', '.'))
        except:
            rec['Avg_Length'] = 0.0

        try:
            rec['Quantity_Stocked'] = int(str(rec['Quantity_Stocked']).replace(',', ''))
        except:
            rec['Quantity_Stocked'] = 0

        # Format Date standard to 'DD-MM-YYYY'
        if rec['Stocking_Date']:
            try:
                date_time_obj = pd.to_datetime(rec['Stocking_Date'], errors='coerce')
                if pd.notna(date_time_obj):
                    rec['Stocking_Date'] = date_time_obj.strftime('%d-%m-%Y')
            except:
                rec['Stocking_Date'] = ""

        cleaned_records.append(rec)

    return pd.DataFrame(cleaned_records)


def save_to_csv(df):
    df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
    return f"Success: All data has been saved to {CSV_FILENAME}"


# ================ STEP 5: Database Lake Validation Check ======================================
def check_lakes_with_name_transfer_logic(df):
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


# ================ STEP 6: Purge Outdated Stocks =================================================
def out_with_the_old(year_to_delete):
    Stock.objects.filter(date_stocked__year=year_to_delete).delete()
    return f"All stocks from {year_to_delete} have been removed"


# ================ STEP 7: DB Stocking Writing Processor ===============================================
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

        # Fish Code Lookup
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

        # Convert back to shortcode for database insertion step
        strain_to_find = str(row['Strain']).strip()
        db_strain_code = ""
        for full_name, code in STRAIN_lookup:
            if strain_to_find.lower() == full_name.lower() or strain_to_find.lower() == code.lower():
                db_strain_code = code
                break
        
        geo = str(row['Genotype']) if str(row['Genotype']) in ("2N", "3N", "AF2N", "AF3N") else ""

        # Validate Date Format Object
        try:
            raw_val = row["Stocking_Date"]
            date_str = str(raw_val).strip()
            
            # This will show you hidden characters like \xa0 or \r
            # print(f"Raw repr: {repr(raw_val)} | Stripped repr: {repr(date_str)}") 
            
            date_object = dt.strptime(date_str, '%d-%m-%Y').date()
        except Exception as e:
            print(f"Failed to parse. Error: {e}\n")
            continue
        
        # print (f'{lake_name_input_clean =}')

        # Save Entry to MariaDB Database
        try:
            stock = Stock(
                date_stocked=date_object, 
                number=stock_number,
                length=row['Avg_Length'],
                lake=lake_id,
                fish=fish_id,
                strain=db_strain_code,
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
# 🚀 CORE RUN TIME EXECUTION
# ==============================================================================
def run():
    YEAR_TO_DELETE = 2026

    
    print(f"Attempting to extract tables via text stream from: {PDF_PATH}")
    raw_lines = extract_pdf_to_raw_rows()
    if not raw_lines:
        print("🛑 STEP 1-2 FAILED: No raw lines extracted from PDF table flow. Check your file path.")
        sys.exit(1)
    print("STEP 1: Successfully read text streams off PDF pages.")

    structured_list = parse_and_structure_rows(raw_lines)
    print("STEP 2: Isolated layout rows using ATS positioning anchors.")

    final_df = standardize_and_clean_records(structured_list)
    print("STEP 3: Text cleaned up, dates normalized, and strains fully written out.")

    message = save_to_csv(final_df)
    print(f"STEP 4: {message}")

    # ⏸️ PAUSE POINT: Allow manual modification of the CSV file
    print("\n======================================================================")
    print(f"⏸️  PAUSED: You can now open '{CSV_FILENAME}' and perform manual edits.")
    print("======================================================================")
    input("👉 Press Enter here to continue once you have manually edited and saved the CSV file...")
    

    # 🔄 RELOAD DATA: Overwrite the DataFrame with your modified CSV data
    print(f"\n🔄 Reloading modified data from '{CSV_FILENAME}'...")
    try:
        final_df = pd.read_csv(CSV_FILENAME, keep_default_na=False)
        print("Successfully reloaded edited data into memory.")
    except Exception as e:
        print(f"🛑 Error reading modified CSV file: {e}")
        sys.exit(1)

    # Proceed with Database validations using the newly reloaded DataFrame
    checked_df, message, unmatched_lakes = check_lakes_with_name_transfer_logic(final_df)
    
    if unmatched_lakes:
        print(f"\n🛑 STOPPING: {len(unmatched_lakes)} lakes were not matched in your local database.")
        print("Please fix or manually verify these ATS tags in your CSV or Database before processing entries.")
        return 
    else:
        print(f"STEP 5: {message}")

    # ==============================================================================
    # 🔓 Database Write Protections
    # (Uncomment the lines below when you are ready to run against your database)
    # ==============================================================================
    message = out_with_the_old(YEAR_TO_DELETE)
    print(f"STEP 6: {message}")

    message = stock_import_process(checked_df)
    print(f"STEP 7: {message}")

    print("--- Stock Record Import Complete ---")