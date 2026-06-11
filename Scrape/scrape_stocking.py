import re
import csv
import asyncio
import requests
from bs4 import BeautifulSoup
import aiohttp

BASE_URL = "https://mywildalberta.ca"
START_URL = f"{BASE_URL}/fishing/fish-stocking/stocking-maps.aspx?listing=1"

def get_main_table_data(url):
    """
    Parses the main list table to extract:
    Waterbody Name, District, Zone Regulations, URL, and Waterbody ID.
    """
    print(f"Fetching main list from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error loading main page: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    if not tables:
        print("Could not find any tables on the page.")
        return []
        
    target_table = None
    for table in tables:
        if table.find('a', href=True, string=True):
            target_table = table
            break
            
    if not target_table:
        print("Could not find a table containing data links.")
        return []

    extracted_rows = []
    
    for row in target_table.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) < 3:
            continue 
            
        a_tag = tds[0].find('a', href=True)
        if not a_tag:
            continue
            
        href = a_tag['href']
        if 'stocking-maps.aspx?id=' in href.lower():
            if href.startswith('/'):
                full_url = BASE_URL + href
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = f"{BASE_URL}/fishing/fish-stocking/{href}"
                
            id_match = re.search(r"[?&]id=(\d+)", href, re.IGNORECASE)
            waterbody_id = id_match.group(1) if id_match else "Unknown"
            
            waterbody_name = tds[0].get_text(strip=True)
            district = tds[1].get_text(strip=True)
            zone_regs = tds[2].get_text(strip=True)
            
            extracted_rows.append({
                "Waterbody ID": waterbody_id,
                "Waterbody Name": waterbody_name,
                "District": district,
                "Zone Regulations": zone_regs,
                "URL": full_url
            })
                
    print(f"Successfully processed {len(extracted_rows)} waterbodies from the main table.")
    return extracted_rows

async def fetch_nested_details(session, item):
    """
    Asynchronously crawls the unique sub-link to find the Surface Area (ha),
    as well as the Latitude and Longitude from the Location text.
    """
    url = item['url']
    
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                return "Error", "Error", "Error"
                
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            page_text = soup.get_text()
            
            # 1. Extract Surface Area value
            sa_match = re.search(r"Surface\s+Area\s*\(ha\):\s*([\d\.]+)", page_text, re.IGNORECASE)
            surface_area = sa_match.group(1) if sa_match else "Not Found"
            
            # 2. Extract Latitude and Longitude from "Location: 52.063523 -115.092202"
            # Captures two distinct floats (positive or negative) following "Location:"
            loc_match = re.search(r"Location:\s*(-?[\d\.]+)\s+(-?[\d\.]+)", page_text, re.IGNORECASE)
            
            if loc_match:
                latitude = loc_match.group(1)
                longitude = loc_match.group(2)
            else:
                latitude = "Not Found"
                longitude = "Not Found"
                
            return surface_area, latitude, longitude
                
    except Exception:
        return "Failed", "Failed", "Failed"

async def enrich_with_nested_data(items):
    """
    Throttles asynchronous sub-page visits to extract data concurrently.
    """
    sem = asyncio.Semaphore(10) # 10 parallel connections max
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        async def worker(item):
            async with sem:
                surface_area, latitude, longitude = await fetch_nested_details(session, item)
                return {
                    "Waterbody ID": item["Waterbody ID"],
                    "Waterbody Name": item["Waterbody Name"],
                    "District": item["District"],
                    "Zone Regulations": item["Zone Regulations"],
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Surface Area (ha)": surface_area,
                    "URL": item["URL"]
                }
                
        for item in items:
            tasks.append(worker({"url": item["URL"], **item}))
            
        return await asyncio.gather(*tasks)

def main():
    items = get_main_table_data(START_URL)
    
    if not items:
        print("No waterbody index data found. Exiting.")
        return

    print("Gathering nested Surface Area and Coordinate metrics...")
    final_results = asyncio.run(enrich_with_nested_data(items))
    
    # Write out to CSV with explicit individual columns
    csv_file = "alberta_lake_stocking_master.csv"
    fieldnames = [
        "Waterbody ID", 
        "Waterbody Name", 
        "District", 
        "Zone Regulations", 
        "Latitude",
        "Longitude",
        "Surface Area (ha)", 
        "URL"
    ]
    
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in final_results:
            writer.writerow(row)
            
    print(f"\nCompleted! Master data cleanly written into separate columns inside '{csv_file}'.")

if __name__ == "__main__":
    main()