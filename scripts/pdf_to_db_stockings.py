import os
import sys
import re
import csv
import shutil
import subprocess
import requests
from datetime import datetime as dt
import pandas as pd
from django.db.models import Q
from django.utils import timezone

# Setup Django if run as standalone script
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FishingLog.settings")
    import django
    django.setup()

from catches.models import Lake, Fish, Stock, Updated
from catches.helpers.fish_data import STRAIN

# --- File Paths & Configurations ---
PDF_URL = "https://open.alberta.ca/dataset/be2e3289-2f94-461d-b4b9-ef50216b8157/resource/0390841a-ae35-4d1c-b6bb-fe04927984ce/download/fp-alberta-fish-stocking-report-2026.pdf"
PDF_PATH = "scripts/fp-alberta-fish-stocking-report-2026.pdf" 
CSV_FILENAME = "scripts/csv_data.csv"

# Target Column Names
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

# Canonical lookup mapping from parsed strain string to DB Strain code
STRAIN_NAME_TO_CODE = {
    'allison creek': 'AC',
    'beitty resort': 'BEBE',
    'beitty x beitty': 'BEBE',
    'beitty/bow river': 'BRBE',
    'bow river': 'BRBE',
    'bow river x beitty': 'BRBE',
    'campbell lake': 'CLCL',
    'ethel lake': 'EL',
    'graham lake': 'GL',
    'job lake': 'JBL',
    'lac ste. anne': 'LSE',
    'lac ste anne': 'LSE',
    'lyndon': 'LYLY',
    'marie creek': 'MC',
    'pit lake': 'PLPL',
    'pit lakes': 'PLPL',
    'riverence': 'RD',
    'riverance': 'RD',
    'rock island': 'RI',
    'trout lodge / jumpers': 'TLTLJ',
    'trout lodge/jumpers': 'TLTLJ',
    'trout lodge / kamloops': 'TLTLK',
    'trout lodge/kamloops': 'TLTLK',
    'trout lodge / silvers': 'TLTLS',
    'trout lodge/silvers': 'TLTLS',
    "trout lodge/silver's": 'TLTLS',
}

# Reverse mapping to display full friendly name in CSV
DB_CODE_TO_FULL_NAME = dict((code, name) for code, name in STRAIN)
# Additional display name overrides for common names
DB_CODE_TO_FULL_NAME.update({
    'BEBE': 'Beitty Resort',
    'BRBE': 'Bow River x Beitty',
    'TLTLJ': 'Trout Lodge / Jumpers',
    'TLTLK': 'Trout Lodge / Kamloops',
    'TLTLS': 'Trout Lodge / Silvers',
    'RD': 'Riverence',
    'PLPL': 'Pit Lakes',
    'AC': 'Allison Creek',
})

SPECIES_CODES = ["RNTR", "CTTR", "WSCT", "WALL", "BKTR", "BNTR", "TGTR"]
GENOTYPE_CODES = ["2N", "3N", "AF2N", "AF3N"]

DATE_RE = re.compile(r'\b(\d{1,2}-[A-Za-z]{3}-\d{2,4})\b')
ATS_RE = re.compile(r'([NESW]{2}\d{1,2}-\d{1,3}-\d{1,2}-(?:W\d)?)', re.IGNORECASE)


# ================ DOWNLOAD ENGINE ==============================================================
def download_pdf(url=PDF_URL, destination=PDF_PATH, force=False):
    """
    Downloads the PDF report directly from open.alberta.ca.
    Skips if local file exists unless force=True.
    """
    if os.path.exists(destination) and not force:
        print(f"ℹ️  PDF already exists locally at '{destination}'.")
        return True

    print(f"⬇️  Downloading stocking report from:\n    {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=16384):
                f.write(chunk)
        print(f"✅ Successfully downloaded PDF ({os.path.getsize(destination):,} bytes) to '{destination}'.")
        return True
    except Exception as e:
        if os.path.exists(destination):
            print(f"⚠️  Download failed ({e}), but using existing local file at '{destination}'.")
            return True
        print(f"🛑 Error downloading PDF from {url}: {e}")
        return False


# ================ EXTRACTION ENGINE ===========================================================
def extract_pdf_layout_text(pdf_path=PDF_PATH):
    """
    Extracts text from PDF preserving 2D column layout using pdftotext.
    Falls back to tabula if pdftotext is not available.
    """
    if shutil.which('pdftotext'):
        try:
            proc = subprocess.run(
                ['pdftotext', '-layout', pdf_path, '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return proc.stdout.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"⚠️  pdftotext execution error: {e}. Falling back to tabula...")
    
    # Fallback to tabula
    try:
        import tabula
        print("Using tabula-py fallback for extraction...")
        dfs = tabula.read_pdf(pdf_path, pages='all', output_format='dataframe', stream=True)
        raw_rows = []
        for df in dfs:
            for _, row in df.iterrows():
                row_text = " ".join([str(v).strip() for v in row.values if pd.notna(v) and str(v).lower() != 'nan'])
                if row_text:
                    raw_rows.append(row_text)
        return "\n".join(raw_rows)
    except Exception as e:
        print(f"🛑 Error reading PDF via tabula: {e}")
        return ""


def parse_layout_text_to_records(layout_text):
    """
    Parses column-aligned layout text.
    Handles multi-line wrapping for:
      - Waterbody Name (e.g. 'Blood Indian Creek' / 'Reservoir')
      - ATS location continuation (e.g. 'SW15-106-12-' / 'W5')
      - Strain names (e.g. 'Trout' / 'Lodge/Kamloops')
    """
    lines = layout_text.splitlines()

    # Filter to table area
    table_lines = []
    in_table = False
    for l in lines:
        if 'FISH STOCKING REPORT' in l or ('Waterbody Name' in l and 'ATS' in l):
            in_table = True
            continue
        if in_table:
            if 'Total Trout Stocked' in l or 'Lakes Stocked to Date' in l:
                break
            if any(ign in l for ign in ['For more information', 'Classification:', '©', '*Strain', '**Gentotype', '\x0c']):
                continue
            if l.strip():
                table_lines.append(l)

    # Group lines by stocking record (anchored by Stocking Date)
    raw_records = []
    current_rec = None
    for l in table_lines:
        if DATE_RE.search(l):
            current_rec = [l]
            raw_records.append(current_rec)
        else:
            if current_rec:
                current_rec.append(l)

    structured_records = []

    for rec_lines in raw_records:
        line1 = rec_lines[0]
        d_m = DATE_RE.search(line1)
        if not d_m:
            continue
        date_str = d_m.group(1)

        ats_m = ATS_RE.search(line1)
        if not ats_m:
            continue

        ats_str = ats_m.group(1).upper()
        lake_part = line1[:ats_m.start()].strip()
        after_ats = line1[ats_m.end():]

        # Identify Species
        sp_found = ""
        sp_start = -1
        sp_end = -1
        for sp in SPECIES_CODES:
            sp_m = re.search(r'\b' + sp + r'\b', after_ats)
            if sp_m:
                sp_found = sp
                sp_start = ats_m.end() + sp_m.start()
                sp_end = ats_m.end() + sp_m.end()
                break

        if not sp_found:
            continue

        after_sp = line1[sp_end:]

        # Identify Genotype
        geno_found = "2N"
        geno_start = -1
        geno_end = -1
        for geno in GENOTYPE_CODES:
            g_m = re.search(r'\b' + geno + r'\b', after_sp)
            if g_m:
                geno_found = geno
                geno_start = sp_end + g_m.start()
                geno_end = sp_end + g_m.end()
                break

        strain_part = line1[sp_end:geno_start].strip() if geno_start != -1 else ""

        # Extract numeric columns (Avg Length, Quantity) between Genotype and Date
        after_geno = line1[geno_end:d_m.start()].strip() if geno_end != -1 else ""
        num_tokens = after_geno.split()
        if len(num_tokens) >= 2:
            length_str = num_tokens[0]
            qty_str = num_tokens[1].replace(',', '')
        elif len(num_tokens) == 1:
            length_str = num_tokens[0]
            qty_str = "0"
        else:
            length_str = "0.0"
            qty_str = "0"

        # Handle Continuation Lines (Lines 2, 3...)
        # Route wrapped text back to its respective column based on character offsets
        for cont_line in rec_lines[1:]:
            lake_cont = cont_line[:ats_m.start()].strip()
            ats_cont = cont_line[ats_m.start():sp_start].strip()
            strain_cont = cont_line[sp_end:d_m.start()].strip()

            if lake_cont:
                lake_part = f"{lake_part} {lake_cont}".strip()
            if ats_cont:
                # Merge wrapped ATS components like '-W5'
                clean_ats_cont = ats_cont.strip('-').upper()
                if not ats_str.endswith(clean_ats_cont):
                    ats_str = f"{ats_str.rstrip('-')}-{clean_ats_cont}"
            if strain_cont:
                strain_part = f"{strain_part} {strain_cont}".strip()

        # Clean multiple spaces inside Lake Name or Strain
        lake_part = re.sub(r'\s+', ' ', lake_part)
        strain_part = re.sub(r'\s+', ' ', strain_part)

        record = {
            'Lake_Name': lake_part,
            'ATS_Location': ats_str,
            'Species_Code': sp_found,
            'Strain': strain_part,
            'Genotype': geno_found,
            'Avg_Length': length_str,
            'Quantity_Stocked': qty_str,
            'Stocking_Date': date_str
        }
        structured_records.append(record)

    return structured_records


# ================ STANDARDIZATION ENGINE ==============================================================
def standardize_and_clean_records(records):
    """
    Standardizes data formats:
    - Normalizes strain names using canonical mapping
    - Converts numbers to proper numeric types
    - Standardizes date strings to DD-MM-YYYY
    """
    cleaned_records = []

    for rec in records:
        raw_strain = rec['Strain'].strip().lower()
        strain_code = STRAIN_NAME_TO_CODE.get(raw_strain)

        # Fallback partial matching if exact dictionary lookup fails
        if not strain_code:
            for name_pattern, code in STRAIN_NAME_TO_CODE.items():
                if name_pattern in raw_strain:
                    strain_code = code
                    break

        if strain_code:
            rec['Strain_Code'] = strain_code
            rec['Strain'] = DB_CODE_TO_FULL_NAME.get(strain_code, rec['Strain'])
        else:
            rec['Strain_Code'] = ""
            rec['Strain'] = rec['Strain'] if rec['Strain'] else "Unknown Strain"

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
    export_df = df.copy()
    if 'Strain_Code' in export_df.columns:
        export_df = export_df.drop(columns=['Strain_Code'])
    export_df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
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
                if db_name == lake_name_input_clean or db_name in lake_name_input_clean or lake_name_input_clean in db_name or db_name == "unnamed":
                    matched_lake = lake
                    break
            if not matched_lake:
                unmatched_lakes.append(row)

    if unmatched_lakes:
        return df, "", unmatched_lakes
    return df, "All lakes checked successfully", unmatched_lakes


# ================ STEP 6: Purge Outdated Stocks =================================================
def out_with_the_old(year_to_delete):
    count, _ = Stock.objects.filter(date_stocked__year=year_to_delete).delete()
    return f"All stocks ({count} records) from {year_to_delete} have been removed"


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
                    db_name = lake.name.strip().lower()
                    if db_name == lake_name_input_clean or db_name in lake_name_input_clean or lake_name_input_clean in db_name or db_name == "unnamed":
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
            fish_abbrev = str(row['Species_Code']).strip().upper()
            if fish_abbrev == "CTTR":
                fish_id = Fish.objects.filter(abbreviation__in=["WSCT", "CTTR"]).first()
            else:
                fish_id = Fish.objects.get(abbreviation=fish_abbrev)
            stock_number = int(row['Quantity_Stocked'])
            
            if fish_id.id in [7, 8, 9, 10, 14]:
                total_non_trout_stocked += stock_number
            else:
                total_trout_stocked += stock_number
        except Exception as e:
            continue

        # Look up DB shortcode for strain
        db_strain_code = row.get('Strain_Code', '')
        if not db_strain_code:
            strain_to_find = str(row['Strain']).strip().lower()
            db_strain_code = STRAIN_NAME_TO_CODE.get(strain_to_find, '')
        
        geo = str(row['Genotype']) if str(row['Genotype']) in ("2N", "3N", "AF2N", "AF3N") else ""

        # Validate Date Format Object
        try:
            raw_val = row["Stocking_Date"]
            date_str = str(raw_val).strip()
            date_object = dt.strptime(date_str, '%d-%m-%Y').date()
        except Exception as e:
            print(f"Failed to parse date '{row.get('Stocking_Date')}'. Error: {e}\n")
            continue

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
    
    last_update = Updated(
        date_stocked=timezone.now().date(),
        number=total_fish_stocked
    )
    last_update.save()

    return f'\n{total_trout_stocked:,} trout stocked\nTotal of {total_fish_stocked:,} fish database writes complete.'


# ==============================================================================
# 🚀 CORE RUN TIME EXECUTION
# ==============================================================================
def run(*args):
    """
    Main execution pipeline:
    1. Automatically downloads PDF from open.alberta.ca (or uses local file).
    2. Extracts and structures tabular data with column-aware positioning.
    3. Normalizes strains, dates, and numbers.
    4. Saves clean CSV backup for audit/inspection.
    5. Validates lake records against the database.
    6. Purges existing stocks for target year.
    7. Imports fresh stocking records into the database.

    Optional args:
      '--force-download': re-download PDF even if present locally
      '--dry-run': validate and save CSV without writing to DB
      '--pause': pause for manual inspection of CSV before DB write
    """
    force_dl = '--force-download' in args
    dry_run = '--dry-run' in args
    pause_for_edit = '--pause' in args
    YEAR_TO_DELETE = 2026

    print("======================================================================")
    print("🎣 Alberta Fish Stocking Automated Import Pipeline")
    print("======================================================================")

    # STEP 0: Download PDF
    if not download_pdf(PDF_URL, PDF_PATH, force=force_dl):
        print("🛑 Pipeline stopped: Unable to obtain PDF report.")
        return

    # STEP 1: Extract 2D layout text
    print(f"\nSTEP 1: Extracting layout text from: {PDF_PATH}")
    layout_text = extract_pdf_layout_text(PDF_PATH)
    if not layout_text:
        print("🛑 STEP 1 FAILED: No text extracted from PDF. Check file and dependencies.")
        return
    print("✅ Text successfully extracted.")

    # STEP 2: Parse and structure rows with column-aware positioning
    print("\nSTEP 2: Parsing rows with column-aligned coordinates...")
    structured_list = parse_layout_text_to_records(layout_text)
    print(f"✅ Isolated {len(structured_list)} stocking entries with complete multi-line recovery.")

    # STEP 3: Standardize & clean
    print("\nSTEP 3: Cleaning text, normalizing strains and dates...")
    final_df = standardize_and_clean_records(structured_list)
    print("✅ Text cleaned, dates normalized, and strains accurately resolved.")

    # STEP 4: Save to CSV
    message = save_to_csv(final_df)
    print(f"\nSTEP 4: {message}")

    # Optional pause point (only if explicitly requested via --pause)
    if pause_for_edit:
        print("\n======================================================================")
        print(f"⏸️  PAUSED: You can now inspect '{CSV_FILENAME}' before DB import.")
        print("======================================================================")
        input("👉 Press Enter here to continue once you have inspected the CSV file...")
        try:
            final_df = pd.read_csv(CSV_FILENAME, keep_default_na=False)
            # Re-apply strain codes if reloaded from CSV
            final_df['Strain_Code'] = final_df['Strain'].astype(str).str.strip().str.lower().map(STRAIN_NAME_TO_CODE).fillna('')
            print("Successfully reloaded CSV data into memory.")
        except Exception as e:
            print(f"🛑 Error reading CSV file: {e}")
            return

    # STEP 5: Validate lakes against database
    print("\nSTEP 5: Validating lakes against database...")
    checked_df, message, unmatched_lakes = check_lakes_with_name_transfer_logic(final_df)
    if unmatched_lakes:
        print(f"\n🛑 STOPPING: {len(unmatched_lakes)} lakes were not matched in your local database:")
        for idx, row in enumerate(unmatched_lakes):
            print(f"   {idx+1}. {row.get('Input_Name_Clean')} (ATS: {row.get('Input_ATS')})")
        return
    print(f"✅ STEP 5: {message}")

    if dry_run:
        print("\n🔎 DRY-RUN complete: No database modifications were performed.")
        return

    # STEP 6: Purge Outdated Stocks for target year
    print(f"\nSTEP 6: Purging existing stocks for year {YEAR_TO_DELETE}...")
    message = out_with_the_old(YEAR_TO_DELETE)
    print(f"✅ STEP 6: {message}")

    # STEP 7: Import records to database
    print("\nSTEP 7: Writing stocks to database...")
    message = stock_import_process(checked_df)
    print(f"✅ STEP 7: {message}")

    print("\n🎉 --- Stock Record Import Complete Successfully! ---")


if __name__ == "__main__":
    cli_args = sys.argv[1:]
    run(*cli_args)