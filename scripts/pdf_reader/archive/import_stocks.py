import tabula
import pandas as pd
import numpy as np
import sqlite3 

# --- Configuration (Constants) ---
PDF_PATH = "epa-alberta-fish-stocking-report-2025.pdf"
CSV_PATH = "clean_stocking_data.csv" # New intermediate file path
DB_NAME = "alberta_stocking_data.db"
TABLE_NAME = "fish_stocking_events"

# 9 elements to match the 9 columns typically extracted by tabula-py.
COL_NAMES = [
    'Lake_Name',           
    'Common_Name',         # Index 1 (Suspect 6: 6-column shift)
    'ATS_Location',        # Index 2 (Suspect 5: 5-column shift)
    'Species_Code',        # Index 3 (Suspect 4: 4-column shift)
    'Strain_Source',       # Index 4 (Suspect 3: 3-column shift)
    'Genotype_Ploidy',     # Index 5 (Suspect 2: 2-column shift)
    'Avg_Length_cm',       # Index 6 (Suspect 1: 1-column shift)
    'Quantity_Stocked',    # Index 7 (Target column for quantity)
    'Stocking_Date'        # Index 8
]

# Index Constants (MUST match the 9-element list)
LAKE_NAME_IDX = 0          
SUPPLIER_STRAIN_IDX = 4    
ATS_LOCATION_IDX = 2       
GENOTYPE_PLOIDY_IDX = 5    
STRAIN_SOURCE_IDX = 4
QTY_IDX = 7                

FOOTER_TEXT_MARKER = "Fish Stocking visit:" 

# --- Function 1: Extraction & Initial Cleaning ---
def process_stocking_report(pdf_path):
    """Extracts tables, merges split rows, and removes footers/artifacts."""
    print(f"1. Attempting to extract tables from: {pdf_path}")
    
    # 1. Extraction (PDF to list of DataFrames)
    try:
        list_of_dfs = tabula.read_pdf(
            pdf_path, 
            pages='all',
            output_format='dataframe',
            multiple_tables=True,
            pandas_options={'header': None} 
        )
    except Exception as e:
        print(f"An error occurred during PDF extraction: {e}")
        return pd.DataFrame() 

    if not list_of_dfs:
        print("No tables were extracted. Returning empty DataFrame.")
        return pd.DataFrame()

    print(f"2. Successfully extracted {len(list_of_dfs)} table(s). Starting cleanup and merge.")
    
    # 2. Cleanup, Merge, and Combine
    combined_dfs = []
    
    for df in list_of_dfs:
        df_merged = df.copy()
        
        # A: MERGE SPLIT DATA (If Supplier/Strain is split across two rows)
        for j in range(len(df_merged) - 1):
            current_row = df_merged.iloc[j]
            next_row = df_merged.iloc[j+1]
            
            if (pd.notna(current_row.iloc[LAKE_NAME_IDX]) and 
                pd.isna(next_row.iloc[LAKE_NAME_IDX]) and 
                pd.notna(next_row.iloc[SUPPLIER_STRAIN_IDX])):
                
                current_value = str(current_row.iloc[SUPPLIER_STRAIN_IDX])
                split_value = str(next_row.iloc[SUPPLIER_STRAIN_IDX])
                
                new_value = f"{current_value}/{split_value}"
                df_merged.iloc[j, SUPPLIER_STRAIN_IDX] = new_value

        # B: REMOVE FOOTER ROWS
        df_merged = df_merged[
            ~df_merged.iloc[:, LAKE_NAME_IDX].astype(str).str.contains(FOOTER_TEXT_MARKER, na=False)
        ]

        # C: REMOVE EMPTY ARTIFACT ROWS
        cleaned_df = df_merged.dropna(subset=[df_merged.columns[LAKE_NAME_IDX]])
        
        combined_dfs.append(cleaned_df)

    if not combined_dfs: return pd.DataFrame()

    final_df = pd.concat(combined_dfs, ignore_index=True)
    
    print(f"3. Cleaning complete. Total raw rows ready for validation: {len(final_df)}.")
    return final_df.reset_index(drop=True)


# --- Function 2: Data Validation and Restructuring ---
def validate_and_reformat_data(df):
    """
    Assigns headers, cleans data types, and applies restructuring logic,
    including fixing column shifts.
    """
    if df.empty: return df

    # 1. REMOVE HEADER ROWS (Deletes the initial two header rows in the combined table)
    df = df.iloc[2:].reset_index(drop=True)
    print("4. Removed the top two header rows.")

    # 2. Assign Headers
    df.columns = COL_NAMES
    print(f"5. Assigned 9 column names: {COL_NAMES}")

    # --- Pre-Cleaning for Shift Detection ---
    
    # Create temporary numeric columns for reliable checks before final formatting.
    df['Quantity_Stocked_TEMP'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['Avg_Length_cm_TEMP'] = pd.to_numeric(
        df['Avg_Length_cm'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['Strain_Source_TEMP'] = pd.to_numeric(
        df['Strain_Source'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['Species_Code_TEMP'] = pd.to_numeric(
        df['Species_Code'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['Genotype_Ploidy_TEMP'] = pd.to_numeric(
        df['Genotype_Ploidy'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['ATS_Location_TEMP'] = pd.to_numeric(
        df['ATS_Location'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    df['Common_Name_TEMP'] = pd.to_numeric(
        df['Common_Name'].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce'
    )
    


    # 3. FIX COLUMN SHIFTING (Multi-Step Robust Logic)
    
    # Condition 1: Quantity is missing/small (<1000) 
    is_qty_missing_or_small = (df['Quantity_Stocked_TEMP'].isna()) | (df['Quantity_Stocked_TEMP'] < 1000)
    
    
    # Step 3.1: FIX C (Check Index 6: Avg_Length_cm, 1-column left shift)
    is_shift_C = is_qty_missing_or_small & (df['Avg_Length_cm_TEMP'] > 1000)
    
    if is_shift_C.any():
        count_C = is_shift_C.sum()
        print(f"   -> Detected and corrected {count_C} rows (Shift C: Index 6 to Index 7 - 1-column shift).")
        df.loc[is_shift_C, df.columns[QTY_IDX]] = df.loc[is_shift_C, df.columns[6]] 
        df.loc[is_shift_C, df.columns[6]] = np.nan 

    
    # Step 3.2: FIX D (Check Index 4: Strain_Source, 3-column left shift) 
    
    # Re-evaluate quantity status based on potential correction from Shift C
    df['Quantity_Stocked_RECHECK_C'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    )
    is_qty_still_missing_D = (df['Quantity_Stocked_RECHECK_C'].isna()) | (df['Quantity_Stocked_RECHECK_C'] < 1000)

    is_shift_D = is_qty_still_missing_D & (df['Strain_Source_TEMP'] > 1000)
    
    if is_shift_D.any():
        count_D = is_shift_D.sum()
        print(f"   -> Detected and corrected {count_D} rows (Shift D: Index 4 to Index 7 - 3-column shift).")
        df.loc[is_shift_D, df.columns[QTY_IDX]] = df.loc[is_shift_D, df.columns[STRAIN_SOURCE_IDX]]
        df.loc[is_shift_D, df.columns[STRAIN_SOURCE_IDX]] = np.nan 

    
    # Step 3.3: FIX A (Check Index 5: Genotype_Ploidy, 2-column left shift) 
    
    # Re-evaluate quantity status based on potential correction from Shift C and D
    df['Quantity_Stocked_RECHECK_CD'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    )
    is_qty_still_missing_A = (df['Quantity_Stocked_RECHECK_CD'].isna()) | (df['Quantity_Stocked_RECHECK_CD'] < 1000)

    is_shift_A = is_qty_still_missing_A & (df['Genotype_Ploidy_TEMP'] > 1000)
    
    if is_shift_A.any():
        count_A = is_shift_A.sum()
        print(f"   -> Detected and corrected {count_A} rows (Shift A: Index 5 to Index 7 - 2-column shift).")
        df.loc[is_shift_A, df.columns[QTY_IDX]] = df.loc[is_shift_A, df.columns[GENOTYPE_PLOIDY_IDX]]
        df.loc[is_shift_A, df.columns[GENOTYPE_PLOIDY_IDX]] = np.nan 

    
    # Step 3.4: FIX E (Check Index 3: Species_Code, 4-column left shift)
    
    # Re-evaluate quantity status based on potential correction from Shift C, D, and A
    df['Quantity_Stocked_RECHECK_CDA'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    )
    is_qty_still_missing_E = (df['Quantity_Stocked_RECHECK_CDA'].isna()) | (df['Quantity_Stocked_RECHECK_CDA'] < 1000)

    is_shift_E = is_qty_still_missing_E & (df['Species_Code_TEMP'] > 1000)
    
    if is_shift_E.any():
        count_E = is_shift_E.sum()
        print(f"   -> Detected and corrected {count_E} rows (Shift E: Index 3 to Index 7 - 4-column shift).")
        df.loc[is_shift_E, df.columns[QTY_IDX]] = df.loc[is_shift_E, df.columns[3]]
        df.loc[is_shift_E, df.columns[3]] = np.nan 


    # Step 3.5: FIX F (Check Index 1: Common_Name, 6-column left shift)
    
    # Re-evaluate quantity status based on potential correction from Shift C, D, A, and E
    df['Quantity_Stocked_RECHECK_CDAE'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    )
    is_qty_still_missing_F = (df['Quantity_Stocked_RECHECK_CDAE'].isna()) | (df['Quantity_Stocked_RECHECK_CDAE'] < 1000)

    is_shift_F = is_qty_still_missing_F & (df['Common_Name_TEMP'] > 1000)
    
    if is_shift_F.any():
        count_F = is_shift_F.sum()
        print(f"   -> Detected and corrected {count_F} rows (Shift F: Index 1 to Index 7 - 6-column shift).")
        df.loc[is_shift_F, df.columns[QTY_IDX]] = df.loc[is_shift_F, df.columns[1]]
        df.loc[is_shift_F, df.columns[1]] = np.nan 


    # Step 3.6: FIX B (Check Index 2: ATS_Location, 5-column left shift - Final check)
    
    # Re-evaluate quantity status based on potential correction from Shift C, D, A, E, and F
    df['Quantity_Stocked_RECHECK_CDEF'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    )
    is_qty_still_missing_B = (df['Quantity_Stocked_RECHECK_CDEF'].isna()) | (df['Quantity_Stocked_RECHECK_CDEF'] < 1000)
    
    is_shift_B = is_qty_still_missing_B & (df['ATS_Location_TEMP'] > 1000)
    
    if is_shift_B.any():
        count_B = is_shift_B.sum()
        print(f"   -> Detected and corrected {count_B} rows (Shift B: Index 2 to Index 7 - 5-column shift).")
        df.loc[is_shift_B, df.columns[QTY_IDX]] = df.loc[is_shift_B, df.columns[ATS_LOCATION_IDX]]
        df.loc[is_shift_B, df.columns[ATS_LOCATION_IDX]] = np.nan 


    # 4. Final Data Type Clean and Column Cleanup
    
    # Convert Quantity to final integer, using the corrected column
    df['Quantity_Stocked'] = pd.to_numeric(
        df['Quantity_Stocked'].astype(str).str.replace(',', '', regex=False), errors='coerce'
    ).fillna(0).astype(int)

    # Convert Avg Length to numeric
    df['Avg_Length_cm'] = pd.to_numeric(
        df['Avg_Length_cm'], errors='coerce'
    ).round(1)

    # Convert Date to datetime format 
    df['Stocking_Date'] = pd.to_datetime(
        df['Stocking_Date'], errors='coerce', dayfirst=True
    )

    # Drop the temporary columns used for checking the shift
    df = df.drop(columns=[
        'Quantity_Stocked_TEMP', 
        'ATS_Location_TEMP', 
        'Genotype_Ploidy_TEMP', 
        'Avg_Length_cm_TEMP', 
        'Strain_Source_TEMP', 
        'Species_Code_TEMP', 
        'Common_Name_TEMP',
        'Quantity_Stocked_RECHECK_C', 
        'Quantity_Stocked_RECHECK_CD',
        'Quantity_Stocked_RECHECK_CDA',
        'Quantity_Stocked_RECHECK_CDAE',
        'Quantity_Stocked_RECHECK_CDEF'
    ], errors='ignore')

    print("6. Final data cleaning complete.")
    return df


# --- Function 3: Tally Stocking Totals ---
def tally_stocking_totals(df):
    """Calculates the total stocked quantity for trout and non-trout species."""
    if df.empty:
        print("No data available to calculate totals.")
        return

    # Official Alberta Trout/Salmonid Species Codes (RNTR=Rainbow, BKTR=Brook, BNTR=Brown, TGTR=Tiger, CTTR=Cutthroat)
    TROUT_CODES = ['RNTR', 'BKTR', 'BNTR', 'CTTR', 'TGTR'] 

    # Create a boolean mask to identify trout rows
    is_trout = df['Species_Code'].str.upper().isin(TROUT_CODES)

    # Calculate totals
    trout_total = df.loc[is_trout, 'Quantity_Stocked'].sum()
    non_trout_total = df.loc[~is_trout, 'Quantity_Stocked'].sum()
    grand_total = df['Quantity_Stocked'].sum()

    print("\n--- 🐟 Fish Stocking Totals ---")
    print(f"Total Trout/Salmonid Stocked: {trout_total:,}")
    print(f"Total Non-Trout Stocked:      {non_trout_total:,}")
    print(f"---------------------------------")
    print(f"GRAND TOTAL STOCKING:         {grand_total:,}")
    print("---------------------------------")


# --- Function 4: CSV Output ---
def save_to_csv(df, csv_path):
    """Saves the final clean DataFrame to a CSV file."""
    if df.empty:
        print("No data to save to CSV.")
        return
    
    try:
        df.to_csv(csv_path, index=False)
        print(f"7. Data successfully written to CSV file: '{csv_path}'.")
    except Exception as e:
        print(f"An error occurred during CSV saving: {e}")


# --- Function 5: Database Loading ---
def load_to_database(df, db_name, table_name):
    """Loads the final clean DataFrame into a SQLite database."""
    if df.empty:
        print("No data to load into the database.")
        return

    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"8. Successfully loaded {len(df)} rows into SQLite database '{db_name}', table '{table_name}'.")
    
    except Exception as e:
        print(f"An error occurred during database loading: {e}")

# ==============================================================================
# 🚀 EXECUTION BLOCK
# ==============================================================================
if __name__ == "__main__":
    
    print("--- Starting Alberta Fish Stocking Data Pipeline ---")
    
    # Step 1: Extract and Clean Raw Data
    raw_df = process_stocking_report(PDF_PATH)
    
    if not raw_df.empty:
        # Step 2: Validate and Reformat Data (Includes header row removal and shift correction)
        clean_df = validate_and_reformat_data(raw_df)
        
        # Step 3: Tally Totals
        tally_stocking_totals(clean_df)
        
        # Step 4 (NEW): Save to CSV for inspection
        save_to_csv(clean_df, CSV_PATH)

        # Step 5: Load to Database
        load_to_database(clean_df, DB_NAME, TABLE_NAME)
    else:
        print("\nProcess halted due to empty data or extraction failure.")
