import re
import csv
import pandas as pd
import tabula

# --- File Paths ---
PDF_PATH = "scripts/fp-alberta-fish-stocking-report-2026.pdf"
OUTPUT_CSV_PATH = "scripts/csv_data_clean.csv"

# --- Target Schema ---
CSV_HEADERS = [
    'Lake_Name',           
    'ATS_Location',        
    'Species_Code',        
    'Strain',       
    'Genotype',     
    'Avg_Length',       
    'Quantity_Stocked',    
    'Stocking_Date'  
]

# --- Master Regular Expressions ---
# A clean, non-capturing pattern to detect any Alberta ATS location code
SIMPLE_ATS_PATTERN = r'(?:[NnSs][EeWw]\d{1,2}-\d{1,3}-\d{1,2}-[Ww]\d{1})'

SPECIES_CODES = ["RNTR", "CTTR", "WSCT", "WALL", "BKTR", "BNTR", "TGTR"]
GENOTYPE_CODES = ["2N", "3N", "AF2N", "AF3N"]

def extract_pdf_to_raw_rows():
    """
    Extracts all pages from the PDF as basic dataframes without enforcing stiff boundaries,
    then normalizes the rows into unified string blocks for pattern checking.
    """
    print(f"Reading tables from: {PDF_PATH}...")
    try:
        # stream=True acts like a text flow reader rather than drawing strict cell bounding boxes
        dfs = tabula.read_pdf(PDF_PATH, pages='all', output_format='dataframe', stream=True)
    except Exception as e:
        print(f"🛑 Error loading file via Tabula: {e}")
        return []

    raw_text_rows = []
    for df in dfs:
        for _, row in df.iterrows():
            # Join the row items into a space-separated text block to eliminate column misalignment
            row_text = " ".join([str(val).strip() for val in row.values if pd.notna(val) and str(val).lower() != 'nan'])
            if row_text:
                raw_text_rows.append(row_text)
                
    return raw_text_rows

def parse_and_structure_rows(raw_rows):
    """
    Sifts through the raw rows, anchors data using the ATS code,
    and intelligently builds structured records out of wrapping lines.
    """
    structured_records = []
    
    current_lake_name = "Unknown"
    current_ats = None

    for line in raw_rows:
        # Check if this row contains a valid ATS code anchoring a stocking record
        ats_match = re.search(SIMPLE_ATS_PATTERN, line)
        
        if ats_match:
            # We found a primary record row!
            current_ats = ats_match.group(0).upper()
            
            # Extract everything before the ATS code as part of the lake name
            line_parts = re.split(SIMPLE_ATS_PATTERN, line, maxsplit=1)
            left_side = line_parts[0].strip()
            right_side = line_parts[1].strip() if len(line_parts) > 1 else ""
            
            # Clean up the lake name (avoiding "Unnamed" or placeholders masking the real text)
            if left_side and left_side.lower() != "unnamed":
                current_lake_name = left_side
            elif not left_side:
                current_lake_name = "Unnamed"

            # Parse out the remaining sequence metrics from the right of the ATS anchor
            right_tokens = right_side.split()
            
            # Basic defaults for safety
            species = ""
            strain = ""
            genotype = ""
            length = "0.0"
            qty = "0"
            date = ""

            # Walk through the items to locate known codes
            for token in right_tokens:
                if token.upper() in SPECIES_CODES:
                    species = token.upper()
                elif token.upper() in GENOTYPE_CODES:
                    genotype = token.upper()
                elif re.match(r'^\d{1,2}-[A-Za-z]{3}-\d{2,4}$', token): # Matches format like 15-Apr-26
                    date = token
                elif "." in token and token.replace('.', '', 1).isdigit():
                    length = token
                elif token.replace(',', '').isdigit():
                    qty = token.replace(',', '')
                else:
                    if token.lower() != "unnamed":
                        strain = f"{strain} {token}".strip()

            # Create our baseline entry
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
            # This is a wrapping line (no ATS code found). It could be an additional stocking run
            # on the same lake, or text overflowing from the previous row elements.
            if not structured_records:
                continue # Skip header/intro lines at the top of the document
                
            last_record = structured_records[-1]
            tokens = line.split()
            
            # Check if this line is an immediate second stocking payload (starts with a species code)
            if tokens and tokens[0].upper() in SPECIES_CODES:
                # Build a brand new row replicating the parent lake context
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
                
                # Sift through remaining line details
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
                # Otherwise, it's just overflowing text (like a split strain description). Append it.
                extra_text = " ".join(tokens)
                if "trout" not in extra_text.lower() and len(extra_text) > 2:
                    if last_record['Strain'] == "Unknown Strain":
                        last_record['Strain'] = extra_text
                    else:
                        last_record['Strain'] = f"{last_record['Strain']} {extra_text}".strip()

    return structured_records

def write_to_csv(records):
    """ Writes structured python dictionaries directly to a standard output CSV file. """
    with open(OUTPUT_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)
    print(f"🎉 Success! Written {len(records)} clean structured rows to: {OUTPUT_CSV_PATH}")

def run():
    raw_lines = extract_pdf_to_raw_rows()
    if not raw_lines:
        print("No lines to parse. Aborting.")
        return
        
    clean_records = parse_and_structure_rows(raw_lines)
    write_to_csv(clean_records)

if __name__ == "__main__":
    run()