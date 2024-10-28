from catches.models import *
from catches.views import *

'''
OLD = [ "Allstones Lake" ,  "Brazeau Borrow Pit #1" ,  "Brazeau Borrow Pit #2" ,  "Brazeau Canal" ,  "Burnstick Lake" ,  
        "Cavan Lake" ,  "Chickakoo Lake" ,  "Chin Lake" ,  "Coleman Fish And Game Pond" ,  "Cottonwood Lake" ,  "Dormer Lake" ,  
        "Eagle Lake" ,  "Gap Lake" ,  "Granum Pond" ,  "Helmer Reservoir" ,  "High Level Community Park Pond" ,  
        "High Level Pond" ,  "Jane Lake" ,  "Jessie Lake" ,  "Keenex Trout Pond" ,  "Keho Lake" ,  "Kinglet Lake" ,  
        "Lac Bellevue" ,  "Lac Delorme" ,  "Lake Newell" ,  "Lake Of Falls" ,  "Landslide Lake" ,  "Little Bow Lake Reservoir" ,  
        "Little Fish Lake" ,  "Lower Kananaskis Lake" ,  "Margaret Lake" ,  "Mcgregor Lake" ,  "Milk River Ridge Reservoir" ,  
        "Mirror Reservoir" ,  "Muskiki Lake" ,  "Oyen Reservoir" ,  "Parker Lake" ,  "Rattlesnake Lake" ,  "Rawson Lake" ,  
        "Sibbald Lake" ,  "Sparrow'S Egg Lake" ,  "St. Mary Reservoir" ,  "Stafford Reservoir" ,  "Tea Lakes" ,  
        "Two Hills Pond" ,  "Upper Champion Lake" ,  "Upper Kananaskis Lake" ,  "Watridge Lake" ,  "Zama Community Pond"]

NONE = ["Abraham Lake" ,  "Aster Lake" ,  "Badger Lake" ,  "Blue Lake" ,  "Boehlke'S Pond" ,  "Bullshead Reservoir " ,  
        "Burns Lake" ,  "Burstall Lakes" ,  "Carnarvon Lake" ,  "Commonwealth Lake" ,  "Entry Lake" ,  "Fortress Lake" ,  
        "Grassi Lake" ,  "Headwall Lakes (Lower)" ,  "Headwall Lakes (Upper)" ,  "Hogarth Lakes Lower" ,  "Hogarth Lakes Upper" ,  
        "Ice Lake" ,  "Invincible Lake" ,  "Lake Of The Falls" ,  "Lake Of The Horns" ,  "Lillian Lake" ,  
        "Little Beaverdam Pond" ,  "Loomis Lake" ,  "Lost Guide Lake" ,  "Lower Champion Lake" ,  "Lower Smuts Lake" ,  
        "Maude Lake" ,  "Md Peace Pond #2" ,  "Memorial Lakes" ,  "Obstruction Lakes" ,  "Odlum Lake" ,  "Quarry Lake" ,  
        "Shark Lake" ,  "Stenton Lake" ,  "Talus Lake" ,  "Three Isle Lake" ,  "Upper Smuts Lake" ,  "Upper Wildhorse Lake" ,  
        "Wedge Pond"]
'''

def get_lakes():
    old = []
    none = []
    lakes = Lake.objects.all()
    for lake in lakes:
        stocks = Stock.objects.filter(lake=lake)
        biggest_year = 0
        for stock in stocks:
            if stock.date_stocked.year > biggest_year:
                biggest_year = stock.date_stocked.year

        if biggest_year != 0 and biggest_year != 2024:  #old
            old.append(lake)

        if biggest_year == 0: #none
            # print (f""" "{lake.name}" """, end =', ')
            none.append(lake)
    return old, none

def check_lakes(name):
    old = ""
    none = ""
    try:
        lake = Lake.objects.get(name = name)
    except:
        return "standard"
    
    stocks = Stock.objects.filter(lake=lake)
    biggest_year = 0
    for stock in stocks:
        if stock.fish.name == "Walleye":
            return "Walleye"
        if stock.date_stocked.year > biggest_year:
            biggest_year = stock.date_stocked.year

    if biggest_year != 0 and biggest_year != 2024:  #old
        return "old"

    if biggest_year == 0: #none
        # print (f""" "{lake.name}" """, end =', ')
        return "never"
        
def read_file(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        
        all_placemarks =  []
        full_placemark = []
        list_of_name = []
        for line in lines:
            full_placemark.append (line)
            # print (line)
            if line.find ('</Placemark>') > -1:
                all_placemarks.append (full_placemark)
                # print (f' ========================== {full_placemark}')
                full_placemark = []
            
            if line.find ('<name>') > -1:
                first_part = line.replace ('<name>', '')
                last_part = first_part.replace ('</name>', '')
                # print (last_part)
                clean_up_start = last_part.replace ('<![CDATA[', '')
                name = clean_up_start.replace (']]>', '')
                list_of_name.append (name.strip())
    list_of_name.sort()

    return list_of_name, all_placemarks

def make_setlist (full_list, old, none):
    lakes_to_change = []
    for o in old:
        if o.name in full_list:
            # print (f'{o} not stocked in 2024')
            lake_set = {
                "lake": o,
                "name": o.name,
                "change": "old"
            }
            lakes_to_change.append (lake_set)
    for n in none:
        if n.name in full_list:
            # print (f'{n} has not been stocked since 2020')
            lake_set = {
                "lake": n,
                "name": n.name,
                "change": "none"
            }
            lakes_to_change.append (lake_set)
    return lakes_to_change
    

def run():
    # OLD = []
    # NONE = []
    
    # # get all lakes that have never been stock or not in 2024
    # OLD, NONE = get_lakes()  

    # read the kml files with all lakes in the map as well a full list of all the placemarks
    full_list, all_placemarks = read_file ('extra files/PART Stocked Lakes.kml')

    # print fill list of all variables.
    # print (f'{len(OLD) = }, {len(NONE) = }, {len(full_list) = }, {len(all_placemarks) = }')

    # make a list of dict of all lakes that need to be changed.
    # lakes_to_change_dict = make_setlist (full_list, OLD, NONE)
    # print (lakes_to_change_dict)

    with open('extra files/PART Stocked Lakes EDIT.kml', "w") as file:
        # Writing data to a file
        for placemark in all_placemarks:
            for line in placemark:
            
                if line.find ('<name>') > -1:
                    first_part = line.replace ('<name>', '')
                    last_part = first_part.replace ('</name>', '')
                    # print (last_part)
                    clean_up_start = last_part.replace ('<![CDATA[', '')
                    name = clean_up_start.replace ("]]>", "")
                    name = name.strip()
                    lake_check = check_lakes (name)
                    print (f'{name} {lake_check = }', end="                                 \r")
                if line.find ('<styleUrl>') > -1:
                    if lake_check == "old":
                        line = "        <styleUrl>#icon-1573-0288D1-nodesc</styleUrl>\n        <description>Has not been stocked in 2024.</description>\n"
                    elif lake_check == "never":
                        line = "        <styleUrl>#icon-1573-795548-nodesc</styleUrl>\n        <description>Has not been stocked since 2020.</description>\n"
                    elif lake_check == "Walleye":
                        line = "        <styleUrl>#icon-1573-F9A825-nodesc</styleUrl>\n        <description>Stocked with Walleye</description>\n"
                    else:
                        line = "        <styleUrl>#icon-1573-0F9D58-nodesc</styleUrl>\n"

                file.writelines(line)
                