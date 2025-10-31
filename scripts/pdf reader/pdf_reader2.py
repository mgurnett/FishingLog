import tabula
import pandas as pd
import os # To manage file paths
import re
from extracter import *

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
CSV_FILENAME = "csv_data.csv"

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
    print(f"Saved table to: {CSV_FILENAME}")

# Step #2 - load csv into dataframe
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

def validate_rows (df):
    df.columns = COL_NAMES
    # print (df.head())
    
    # Create an empty DataFrame
    clean_rows_list = []
    df_new = pd.DataFrame(columns=COL_NAMES)

    # --- While Loop Implementation ---
    index = 0
    mystry_rows = 0
    total_rows = len(df)
    rows_summery = []

    # print("Starting while loop iteration...")
    while index < total_rows:

        print (f'{index} of {total_rows}')


        # 1. Access the current row using .iloc[]
        current_row = df.iloc[index]
    
        # Check to see if ats is there.
        found_ats = check_row_for_ats(current_row) #True if at least one cell contains a valid ATS code, False otherwise.
        
        # declare this to be a main row
        if found_ats:
            row_make_up = {"index":index, "row_type": 'main'}
        else:
            found_data = check_row_for_data (current_row)
            if found_data:
                print('====data row====')
                row_make_up = {"index":index, "row_type": 'data'}
            else:
                row_make_up = {"index":index, "row_type": 'empty'}

        rows_summery.append(row_make_up)
        print (f'{index} of {total_rows} {row_make_up}')
        index +=1

    print (f'{rows_summery}')
        
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
    validate_rows (raw_df)
    # print (cleanedup_df.head)

