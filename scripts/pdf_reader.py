import tabula
import pandas as pd
import os # To manage file paths
import re

# --- Configuration ---
PDF_PATH = "scripts/fp-alberta-fish-stocking-report-2026.pdf" 
CSV_FILENAME = "scripts/csv_data.csv"
CSV_FILENAME_ident = "scripts/csv_data_ident.csv"
CSV_FILENAME_final = "scripts/csv_data_ident.csv"


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

ATS_PATTERN = r'^[NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-W\d{1}$'
SIMPLE_ATS_PATTERN = r'([NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
AVG_LENGTH_PATTERN = r'(\d{1,3}[.,]\d{1,2})'
# Quantity Pattern: Targets the large number with optional commas
QTY_PATTERN = r'(\d{1,3}(?:,\d{3})*)'
# Date Pattern (D-Mon-YY format)
DATE_PATTERN = r'(\d{1,2}\s*[\-\/]\s*[A-Za-z]{3}\s*[\-\/]\s*\d{2,4})'


def extract_and_save_tables():
    print(f"Attempting to extract tables from: {PDF_PATH}")
    
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
        print(f"An error occurred during PDF extraction: {e}")
        return

    if not list_of_dfs:
        print("No tables were extracted. Check your PDF and extraction parameters.")
        return

    print(f"Successfully extracted {len(list_of_dfs)} table(s).")
    
    # ===============================================
    # OPTION B: Combine All Tables and Save to One CSV
    # ===============================================
    print("\n--- Combining and Saving to One File ---")
    
    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    
    # Save the combined DataFrame to a single CSV file
    combined_df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
    print(f"Saved all {len(list_of_dfs)} tables combined to: {CSV_FILENAME}")


def load_csv_to_dataframe():    # --- Core Function: Data Loading ---
    """
    Loads the data from the specified CSV path into a pandas DataFrame.
    
    Args:
        CSV_FILENAME (str): The path to the CSV file (e.g., 'csv_data.csv').
        
    Returns:
        pd.DataFrame: The raw DataFrame loaded from the CSV, or an empty DataFrame if the file is not found.
    """
    if not os.path.exists(CSV_FILENAME):
        print(f"Error: Required file '{CSV_FILENAME}' not found.")
        print("Please ensure you run the extraction script first to create the CSV!")
        return pd.DataFrame()

    print(f"1. Loading raw data from: {CSV_FILENAME}")
    # Read the CSV, skipping the two known header rows, but treating the first row as data
    # (header=None) so we can refer to columns by index (0, 1, 2, etc.) easily.
    df = pd.read_csv(CSV_FILENAME, header=None, skiprows=3)
    
    return df


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


    # Save to your new filename
    df.to_csv("csv_data_ident_2.csv", index=False, encoding='utf-8')
    print("Success: csv_data_ident_2.csv has been created with merged strains.")
    return df


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
        ffull_row_string = ' '.join(str(val) for val in string_series.values if pd.notna(val))
        
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
    final_df.to_csv("csv_data_final.csv", index=False, encoding='utf-8')
    print("Success: csv_data_final.csv has been created.")
    return final_df


        
# ==============================================================================
# 🚀 EXECUTION
# ==============================================================================
def run():
    # Step 1: Load the CSV into a raw DataFrame
    extract_and_save_tables()
    
    # Step 2: Load csv into dataframe
    raw_df = load_csv_to_dataframe()
        
    # The DataFrame 'stocking_df' is now ready for further analysis
    if not raw_df.empty:
        print("\nDataFrame ready for next step!")

    # Step 3: Sort out issues with reading PDF and clean up rows
    cleanedup_df = validate_all_data (raw_df)
    # print (cleanedup_df.head)

    final_df = validate_and_clean_row (cleanedup_df)

    # Save to your new filename
    final_df.to_csv(CSV_FILENAME_final, index=False, encoding='utf-8')
    print("Success: csv_data_final.csv has been created.")