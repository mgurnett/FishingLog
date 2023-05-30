from catches.models import *
import re
from datetime import datetime

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
    ('Job Lake', 'JBL')
 ]
STRAIN = (
    ("BEBE", "Beitty x Beitty"),
    ("BRBE", "Bow River x Beitty"),
    ("CLCL", "Campbell Lake"),
    ("LYLY", "Lyndon"),
    ("PLPL", "Pit Lake"),
    ("TLTLJ", "Trout Lodge / Jumpers"),
    ("TLTLK", "Trout Lodge / Kamloops"),
    ("TLTLS", "Trout Lodge / Silvers"),
    ("LSE", "Lac Ste. Anne"),
    ("JBL", "Job Lake"),
)

def get_data(file_name, year):
    stock_num = 0
    with open(file_name) as file:
        file_contents = file.read()
    
    if year == 0:
        pattern = '(\d{1,2})[-][A-Z][a-z][a-z]-20'
    if year == 1:
        pattern = '(\d{1,2})[/][A-Z][a-z][a-z]/21'
    if year == 2:
        pattern = '(\d{1,2})[-][A-Z][a-z][a-z]-22'
    if year == 3:
        pattern = '(\d{1,2})[-][A-Z][a-z][a-z]-23'

    lines = []
    new_end = 0
    for x in re.finditer (pattern, file_contents):  #find where the line ends as the date is aways the end
        start, end = x.span()
        date_obj = x.group()
        if year == 1:
            stock_date = datetime.strptime(date_obj, "%d/%b/%y") #for 2021
        else:
            stock_date = datetime.strptime(date_obj, "%d-%b-%y") #for 2022 & 3

        row = str(file_contents[new_end:end]) #get the whole row
        # print (row)

        location = re.search ('[NS][EW](\d{1,2})-(\d+)-(\d{1,2})-W[0-9]', row)  #search for the ATS
        if location:
            try:
                lake_id = Lake.objects.get(ats=location.group())
            except:
                print (location.group()," was not found lake database!", row)  #ats not found in database
        else:
            print (row, "******", location) #ats not found in row

        fish_group = re.search (' [A-Z][A-Z][A-Z][A-Z] ', row)
        fish = fish_group.group().strip()
        if fish_group:
            fish_start, fish_end = fish_group.span()
            try:
                fish_id = Fish.objects.get(abbreviation=fish)
            except:
                print (fish," was not found in fish database!")  #ats not found in database
                fish_id = ""
        else:
            print (row, "******", fish) #fish not found in row

        genotype_group = re.search ('[A][F][2-3][N]', row)
        if genotype_group:
            genotype = genotype_group.group()
            geno_start, geno_end = genotype_group.span()
        else:
            genotype_group = re.search ('[2-3][N]', row)
            genotype = genotype_group.group()
            geno_start, geno_end = genotype_group.span()
        # print (genotype)

        strain = str(row[fish_end:geno_start]).strip()

        found=0
        strain_short = ""
        for index, str_look in enumerate(STRAIN_lookup):
            if strain == str_look[0]:
                found=index
        if found == 0:
            print (f'{strain} was not found in {row}')
            pass
        else:
            strain_short = STRAIN_lookup[found][1]
        # print (row, "  ", fish_end, "  ", geno_start, "  ", strain_short)

        length_string = str(row[geno_end:])
        
        fish_str = re.search ("\d*\.?\d+", length_string)
        # print (fish_length, " ", row, " ", length_string)
        fish_len = fish_str.group()
        fish_length = float(fish_len)
        len_start, len_end = fish_str.span()
        # print (f'len_start = {len_start} len_end = {len_end} and fish_len is {fish_len} of length_string {length_string}')

        raw_number = str(length_string[len_end:])
        number_fish = re.search ("\d*\,?\d+", raw_number)
        number_of_fish = int(number_fish.group().replace(",", ""))
        # print (f'number of fish is {number_of_fish} of row {row}')

        new_end = end + 1 #get set to read the next row

        lines.append ([row, stock_date, lake_id, fish_id, genotype, strain_short, fish_length, number_of_fish])
        stock_num += 1
    print (stock_num)
    return lines

def run():
    data2020 = get_data('static/stock_reports/2020_raw.txt', 0)
    print ("2020 is good")
    data2021 = get_data('static/stock_reports/2021_raw.txt', 1)
    print ("2021 is good")
    data2022 = get_data('static/stock_reports/2022_raw.txt', 2)
    print ("2022 is good")
    data2023 = get_data('static/stock_reports/2023_raw.txt', 3)
    print ("2023 is good")

    total_data = data2020 + data2021 + data2022 + data2023

    # print (total_data)

    # with open(r'stock_inputs.txt', 'w') as fp:

    #     for row in total_data:
    #         stock = Stock (
    #             date_stocked = row[1],
    #             number = row[7],
    #             length = row[6],
    #             lake = row[2],
    #             fish = row[3],
    #             strain = row[5],
    #             gentotype = row[4],
    #         )
    #         print (stock)
    #         fp.write("%s\n" % stock)

    Stock.objects.all().delete()

    for row in total_data:
        stock = Stock (
            date_stocked = row[1],
            number = row[7],
            length = row[6],
            lake = row[2],
            fish = row[3],
            strain = row[5],
            gentotype = row[4],
        )
        stock.save()
