import tabula
import pandas as pd
import os # To manage file paths
import re

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

SIMPLE_ATS_PATTERN = r'([NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'
AVG_LENGTH_PATTERN = r'(\d{1,3}[.,]\d{1,2})'
# Quantity Pattern: Targets the large number with optional commas
QTY_PATTERN = r'(\d{1,3}(?:,\d{3})*)'
# Date Pattern (D-Mon-YY format)
DATE_PATTERN = r'(\d{1,2}\s*[\-\/]\s*[A-Za-z]{3}\s*[\-\/]\s*\d{2,4})'


def is_valid_ats_code(text):
    ATS_PATTERN = r'^[NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-W\d{1}$'
    """
    Checks if a given string matches the required ATS location code pattern.
    """
    return bool(re.match(ATS_PATTERN, text))



def check_row_for_data(row: pd.Series) -> bool:
    """
    Efficiently checks all cell values in a pandas Series (a DataFrame row) 
    to see if any value contains characters other than just commas (and is not NaN/None).

    This is useful for identifying rows that are effectively empty (e.g., all cells 
    are NaN, None, or only contain commas like ',,,' or just empty strings).

    Args:
        row: A single row from a pandas DataFrame (pd.Series).

    Returns:
        True if at least one cell contains non-comma data, False otherwise.
    """
    # Pattern to find: one or more characters that are NOT a comma.
    # [^,] means "any character except a comma"
    # + means "one or more times"
    NON_COMMA_PATTERN = r'[^,]+'
    
    
    # 1. Convert all non-string values to strings for consistency.
    #    NaNs will become the string 'nan'.
    # string_series = row.astype(str)
    # string_series = (row.fillna('').astype(str))
    string_series = row.fillna('').astype(str).str.strip()
    # print (string_series)
    
    # 2. Use vectorized string operations for speed.
    #    .str.contains(pattern) returns a boolean Series (True if the string contains the pattern).
    #    na=False ensures that actual NaN values (if they somehow slipped through astype(str))
    #    or string 'nan' (from astype(str)) do not accidentally get a 'True' result, though
    #    'nan' doesn't match the pattern anyway.
    matches = string_series.str.contains(NON_COMMA_PATTERN, na=False)
    
    # 3. Check if ANY cell in the row matched the pattern
    return matches.any()


def check_for_and_cleanup_name (string_series: str) -> str:
    if string_series['Lake_Name'] != "Unnamed":
        return string_series['Lake_Name']
    else:
        return string_series['Common_Name']



