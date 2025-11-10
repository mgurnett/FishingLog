# import tabula
import pandas as pd
import os # To manage file paths
import re
from extracter import *
from typing import Optional

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

ROW_TYPE = ['main,', 'data', 'empty', 'unknown']

# --- Configuration ---
PDF_PATH = "epa-alberta-fish-stocking-report-2025.pdf" 
CSV_FILENAME_RAW = "csv_data_raw.csv"
CSV_FILENAME_FILTERED = "csv_data_filtered.csv"

# Step #1 - convert all PDF rows to csv and save CSV 
def extract_and_save_tables():
    print(f"Attempting to extract tables from: {PDF_PATH}")
    
    # 1. Extraction: Get the DataFrame
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

    print(f"Successfully extracted {len(list_of_dfs)} table.")
    
    # ===============================================
    # Save to CSV
    # ===============================================
    print("\n--- Saving to One File ---")
    
    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    
    # Save the combined DataFrame to a single CSV file
    combined_df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
    print(f"Saved table to: {CSV_FILENAME_RAW}")

# Step #2 - load csv into dataframe
def load_csv_to_dataframe():    # --- Core Function: Data Loading ---
    """
    Loads the data from the specified CSV path into a pandas DataFrame.
    
    Args:
        CSV_FILENAME (str): The path to the CSV file (e.g., 'csv_data.csv').
        
    Returns:
        pd.DataFrame: The raw DataFrame loaded from the CSV, or an empty DataFrame if the file is not found.
    """
    if not os.path.exists(CSV_FILENAME_RAW):
        print(f"Error: Required file '{CSV_FILENAME_RAW}' not found.")
        print("Please ensure you run the extraction script first to create the CSV!")
        return pd.DataFrame()

    print(f"1. Loading raw data from: {CSV_FILENAME_RAW}")
    # Read the CSV, skipping the two known header rows, but treating the first row as data
    # (header=None) so we can refer to columns by index (0, 1, 2, etc.) easily.
    df = pd.read_csv(CSV_FILENAME_RAW, header=None, skiprows=3)
    
    return df




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

        if main_row and not aux_row: # this means that the row is single
            cleaned_current_row = validate_and_clean_row(current_row, None)
            clean_rows_list.append(cleaned_current_row)
            index +=1

        elif main_row and aux_row: #this means that the two rows should be one row
            # print (f'{index} of {total_rows} {advance_row}')
            cleaned_current_row = validate_and_clean_row(current_row, advance_row)
            clean_rows_list.append(cleaned_current_row)
            index +=2

        elif main_row and not aux_row: #this means that the second row is stand alone
            index +=1

        else: # this means that the row read is an aux line
            index +=1

        main_row = False; aux_row = False

    df_new = pd.DataFrame(clean_rows_list, columns=COL_NAMES)
    return df_new


def check_row_for_ats(row: pd.Series) -> bool:
    ATS_PATTERN = r'^[NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-W\d{1}$'
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


def check_row_for_keywords(row: pd.Series) -> str:
    """
    Checks if a row contains the specific keywords "Lodge/Jumpers" or 
    "Lodge/Kamloops" in any cell.

    Args:
        row: A single row from a pandas DataFrame (pd.Series).

    Returns:
        The keyword string found ("Lodge/Jumpers" or "Lodge/Kamloops").
        Returns an empty string ('') if neither is found.
    """
    
    # Define the target keywords
    TARGET_JUMPERS = "Lodge/Jumpers"
    TARGET_KAMLOOPS = "Lodge/Kamloops"
    
    # Robust Cleaning: Replace NaN with empty string, convert all to string, 
    # and strip leading/trailing whitespace.
    string_series = row.fillna('').astype(str).str.strip()
    
    # Iterate through the cleaned string values to check for keywords
    for cell_value in string_series.values:
        if TARGET_JUMPERS in cell_value:
            return TARGET_JUMPERS
        if TARGET_KAMLOOPS in cell_value:
            return TARGET_KAMLOOPS
    return None


def validate_rows(df: pd.DataFrame, COL_NAMES: list, check_row_for_ats) -> pd.DataFrame:
    """
    Validates, cleans, and merges supplementary keyword data into the preceding 
    main data row's 'Strain' column.
    """
    df.columns = COL_NAMES
    
    # Define the index of the 'Strain' column (0-indexed: Strain is the 5th column)
    STRAIN_COLUMN_INDEX = 4 

    clean_rows_list = []
    rows_summery = []
    last_main_data_row_index = -1 # Keep track of the index of the last main data row
    
    index = 0
    total_rows = len(df)
    
    print("Starting row validation and merging...")

    while index < total_rows:
        current_row = df.iloc[index].copy() # IMPORTANT: Use .copy() to allow modification
        row_summary_entry = {"index": index, "row_type": 'unknown'}
        
        found_ats = check_row_for_ats(current_row) 
        keyword_found = check_row_for_keywords(current_row) 
        
        if found_ats:
            # 🥇 CASE 1: Main Data Row (Has ATS)
            row_summary_entry["row_type"] = 'main_data'
            
            # Add the row to the list (it's the primary record)
            clean_rows_list.append(current_row)
            
            # Update the index of the last primary row for future merges
            last_main_data_row_index = len(clean_rows_list) - 1 
            
        elif not found_ats and keyword_found:
            # 🥉 CASE 2: Supplementary Keyword Row (No ATS, Has Keyword)
            row_summary_entry["row_type"] = f'supplementary_keyword: {keyword_found}'
            
            if last_main_data_row_index != -1:
                # Get the *last added* main data row from the clean_rows_list
                target_row = clean_rows_list[last_main_data_row_index]
                
                # MERGE LOGIC: Prepend the keyword to the 'Strain' cell (index 4)
                current_strain = str(target_row.iloc[STRAIN_COLUMN_INDEX]).strip()
                
                if current_strain.lower() in ('trout', 'riverence'):
                    # Overwrite the generic "Trout" or "Riverence" with the specific keyword
                    new_strain_value = f'Trout {keyword_found}'
                else:
                    # Append the keyword to the current strain value
                    new_strain_value = f'Trout {keyword_found}'

                # Update the value in the list of clean rows
                target_row.iloc[STRAIN_COLUMN_INDEX] = new_strain_value
                
                print(f"    -> MERGED: Keyword '{keyword_found}' appended to Strain of row {index-1}.")
            
            # NOTE: Supplementary rows are NOT added to the final list.
            
        else:
            # 👻 CASE 3: Empty or Garbage Row (No ATS, No Keywords)
            row_summary_entry["row_type"] = 'empty_or_garbage'

        # Record the summary and advance the index
        rows_summery.append(row_summary_entry)
        print(f'{index} of {total_rows} {row_summary_entry}')
        index += 1
    
    # Convert the list of clean, now-merged rows into a new DataFrame
    df_new = pd.DataFrame(clean_rows_list, columns=COL_NAMES)
    
    print("\n--- Summary of All Rows ---")
    print(pd.DataFrame(rows_summery).to_markdown(index=False))

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
    df_new = validate_rows (raw_df, COL_NAMES, check_row_for_ats)
    print (df_new.head)

    # Step 4: save the df to a new csv
    df_new.to_csv(CSV_FILENAME_FILTERED, index=False, encoding='utf-8')
