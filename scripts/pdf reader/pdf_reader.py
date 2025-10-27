import tabula
import pandas as pd
import os # To manage file paths
import re

# --- Configuration ---
PDF_PATH = "epa-alberta-fish-stocking-report-2025.pdf" 
CSV_FILENAME = f"csv_data.csv"

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

SPECIES_CODES = ["RNTR", "CTTR", "WALL", "BKTR", "BNTR", "TGTR"]

GENOTYPE_CODES = ["2N", "3N", "AF2N", "AF3N"]

# Define the expected pattern for a valid ATS (Alberta Township Survey) location code.
# Format example: SW4-36-8-W5
# Regex breakdown:
# ^          # Start of string
# [NESW]{2} # Quarter section (e.g., NE, SW)
# \d{1,2}    # Section number (1-36)
# -          # Dash separator
# \d{1,3}    # Township number (e.g., 5, 36)
# -          # Dash separator
# \d{1,2}    # Range number (e.g., 1, 17)
# -          # Dash separator
# W\d{1}     # West of Meridian (W4, W5, W6)
# $          # End of string
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


def check_row_for_ats(row: pd.Series) -> bool:
    """
    Efficiently checks all cell values in a pandas Series (a DataFrame row) 
    to see if any value is a valid ATS location code.

    Args:
        row: A single row from a pandas DataFrame (pd.Series).

    Returns:
        True if at least one cell contains a valid ATS code, False otherwise.
    """
    # 1. Convert all non-string values (like numbers or NaNs) to strings for consistency.
    #    This ensures the .str accessor works cleanly across the entire row.
    string_series = row.astype(str)
    
    # 2. Use vectorized string operations for speed (much faster than looping).
    #    .str.match(pattern) returns a boolean Series (True if the whole string matches the pattern).
    matches = string_series.str.match(ATS_PATTERN, na=False)
    
    # 3. Check if ANY match was found in the row.
    return matches.any()


def validate_and_clean_row(row: pd.Series):
    print ("===== cleaning a single row ======")
    row_dict = {'Lake_Name': "", 'Common_Name': "", 'ATS_Location': "", \
        'Species_Code': "", 'Strain': "", 'Genotype': "", 'Avg_Length': "", 'Quantity_Stocked': "", 'Stocking_Date': ""}

    string_series = row.astype(str)
    # print (string_series)

    # --- 1. Clean Lake Name (Logic is correct here as it uses direct string access) ---
    if string_series['Lake_Name'] != "Unnamed":
        row_dict['Lake_Name'] = string_series['Lake_Name']
    else:
        row_dict['Lake_Name'] = string_series['Common_Name']
    
    
    # --- 2. Robust ATS Location Extraction ---
    
    # Concatenate all string values in the row into ONE string
    full_row_string = ' '.join(string_series.values)

    try:
        # Convert the single Python string into a Series of length 1
        full_row_series = pd.Series([full_row_string])
        
        # Apply .str.extract() to the single, combined string
        extracted_ats = full_row_series.str.extract(SIMPLE_ATS_PATTERN, expand=False).iloc[0]
        
        if pd.isna(extracted_ats):
            # If the extraction is NaN, log the source string for debugging
            print(f"DEBUG: Failed to find ATS in: '{full_row_string[:100]}...'")
            row_dict['ATS_Location'] = "ATS_MISSING_ERROR" 
        else:
            # Clean up the extracted string (remove extra spaces caught by the pattern)
            row_dict['ATS_Location'] = extracted_ats.replace(' ', '').strip()
            
    except Exception as e:
        print(f"Error during robust ATS extraction: {e}")
        row_dict['ATS_Location'] = "ATS_EXTRACTION_ERROR"

    # --- 3. Validate and Extract Species Code ---
    pattern = '|'.join(SPECIES_CODES)
    
    # The value is a Python string, so we convert it to a Series
    species_series = pd.Series([string_series['Species_Code']])
    
    try:
        # Apply .str.contains() to the temporary Series
        # .iloc[0] gets the single True/False result
        is_species_present = species_series.str.contains(pattern, case=True, regex=True).iloc[0]

        if is_species_present:
            # If the code is found, use the value from the row
            row_dict['Species_Code'] = string_series['Species_Code']
        else:
            row_dict['Species_Code'] = "Invalid"

    except Exception as e:
        print(f"Error checking Species Code: {e}")
        row_dict['Species_Code'] = "Not found" 

    # --- 4. Validate and Extract Genotypes Code (CORRECTED) ---

    # 1. Build the pattern using your GENOTYPE_CODES
    pattern = '|'.join(GENOTYPE_CODES)

    # 2. Get the raw string value you want to check
    genotype_val = string_series['Genotype'].strip()
    genotype_series = pd.Series([genotype_val]) # Create a temporary Series for .str methods

    try:
        # Apply .str.contains() to the temporary Genotype Series
        # We check if the Genotype value contains any of the valid codes.
        is_genotype_present = genotype_series.str.contains(pattern, case=False, regex=True).iloc[0]
        
        # We use case=False because codes like 'AF3N' might appear as 'af3n'

        if is_genotype_present:
            # If a valid code is found, use the value from the row (cleaned)
            row_dict['Genotype'] = genotype_val.upper()
        else:
            row_dict['Genotype'] = "Invalid"

    except Exception as e:
        # If anything unexpected goes wrong during checking
        # print(f"Error checking Genotype Code: {e}")
        row_dict['Genotype'] = "Not found"   

    # --- 6. Validate and Extract length ---

    try:
        # 1. Apply extraction across the combined row string
        full_row_series = pd.Series([full_row_string])
        extracted_length_series = full_row_series.str.extract(AVG_LENGTH_PATTERN, expand=False)
        
        # 2. Get the scalar value and clean it
        extracted_length = extracted_length_series.iloc[0]

        if pd.notna(extracted_length):
            # Remove any commas, replace decimal comma with a dot, and convert to float
            cleaned_length_str = extracted_length.replace(',', '').replace('.', '.', 1) 
            row_dict['Avg_Length'] = float(cleaned_length_str)
            
    except IndexError:
        # No match found (extracted_length_series was empty)
        pass
    except ValueError:
        # Matched a number that wasn't a valid float after cleaning
        pass
    except Exception as e:
        # Catch any other unexpected error
        # print(f"Error processing Avg_Length: {e}") 
        pass

    # --- 7. Robust Quantity Stocked Extraction (HEURISTIC: Second-to-Last Column) ---
    row_dict['Quantity_Stocked'] = 0 # Default value is integer 0

    string_series['Quantity_Stocked']

    try:
        # 1. Use the .replace() method to remove the comma
        string_without_comma = string_series['Quantity_Stocked'].replace(',', '')

        # 2. Use the int() function to convert the cleaned string to an integer
        row_dict['Quantity_Stocked'] = int(string_without_comma)
                    
    except Exception as e:
        # print(f"Quantity Exception: {e}")
        pass # Suppress error and maintain default 0
    
    # --- 8. Robust Stocking Date Extraction (CORRECTED LOGIC) ---
    try:
        # Extract the date string using the pattern on the single-element Series.
        # This returns a Series of length 1 (containing the date string or NaN).
        extracted_date_series = full_row_series.str.extract(DATE_PATTERN, expand=False)
        
        # Get the single scalar value from the Series.
        extracted_date = extracted_date_series.iloc[0]
        
        # Check if a date was actually found (pd.notna handles the NaN case)
        if pd.notna(extracted_date):
            
            # Use pandas.to_datetime for robust parsing
            # errors='coerce' turns bad date strings into NaT
            date_time_obj = pd.to_datetime(extracted_date, errors='coerce')
            
            if pd.notna(date_time_obj):
                # Save as a standardized YYYY-MM-DD string
                row_dict['Stocking_Date'] = date_time_obj.strftime('%Y-%m-%d')
                
    except Exception as e:
        # Optional: Add a print statement here to see what exception is being suppressed
        # print(f"Date Exception: {e}")
        pass # Date remains None



    # 'Strain',       

    print(f"ATS = {row_dict['ATS_Location']} and species is {row_dict['Species_Code']} and length is {row_dict['Avg_Length']} \
    {row_dict['Genotype']} # {row_dict['Quantity_Stocked']} on: {row_dict['Stocking_Date']}")

    return row_dict


def validate_all_data (df):

    df.columns = COL_NAMES
    # print (df.head())
    
    # Create an empty DataFrame
    clean_rows_list = []
    df_new = pd.DataFrame(columns=COL_NAMES)

    # --- While Loop Implementation ---
    index = 0
    total_rows = len(df)
    main_row = False; aux_row = False; 

    # print("Starting while loop iteration...")
    while index < total_rows:
        # 1. Access the current row using .iloc[]
        current_row = df.iloc[index]
        # print (f'{index} of {total_rows} {current_row}')
    
        # Run the check function
        found_ats = check_row_for_ats(current_row) #True if at least one cell contains a valid ATS code, False otherwise.
        
        # declare this to be a main row
        if found_ats:
            # print(f"  -> Match found in row: {current_row.to_dict()}")
            main_row = True
            cleaned_current_row = validate_and_clean_row(current_row)
            clean_rows_list.append(cleaned_current_row)
        
        try:
            advance_row = df.iloc[index + 1]
        except:
            pass
        else:
            found_ats = check_row_for_ats(advance_row) #True if at least one cell contains a valid ATS code, False otherwise.
            if found_ats:
                aux_row = False
            else:
                aux_row = True

        if main_row and aux_row: #this means that the two rows should be one row
            index +=2
            # print (f'{index} of {total_rows} {advance_row}')

        elif main_row and not aux_row: #this means that the second row is stand alone
            index +=1

        else: # this means that the row read is an aux line
            index +=1

        main_row = False; aux_row = False

    df_new = pd.DataFrame(clean_rows_list, columns=COL_NAMES)
    return df_new


        
# ==============================================================================
# 🚀 EXECUTION
# ==============================================================================
if __name__ == "__main__":
    # Step 1: Load the CSV into a raw DataFrame
    # extract_and_save_tables()
    
    # Step 2: Load csv into dataframe
    raw_df = load_csv_to_dataframe()
        
    # The DataFrame 'stocking_df' is now ready for further analysis
    if not raw_df.empty:
        print("\nDataFrame ready for next step!")

    # Step 3: Validate each line of data
    cleanedup_df = validate_all_data (raw_df)
    # print (cleanedup_df.head)

