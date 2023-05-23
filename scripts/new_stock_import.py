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

def get_data():
    with open('static/stock_reports/2021_raw.txt') as file:
        file_contents = file.read()

    lines = []
    new_end = 0
    for x in re.finditer ('(\d{1,2})[/][A-Z][a-z][a-z]/21', file_contents):  #find where the line ends as the date is aways the end
        start, end = x.span()
        date_obj = x.group()
        stock_date = datetime.strptime(date_obj, "%d/%b/%y")

        row = str(file_contents[new_end:end]) #get the whole row

        location = re.search ('[NS][EW](\d{1,2})-(\d+)-(\d{1,2})-W[0-9]', row)  #search for the ATS
        if location:
            try:
                lake_id = Lake.objects.get(ats=location.group())
            except:
                print (location.group()," was not found lake database!", row)  #ats not found in database
        else:
            print (row, "******", location) #ats not found in row

        fish_group = re.search ('[A-Z][A-Z][A-Z][A-Z]', row)
        fish = fish_group.group()
        if fish_group:
            fish_start, fish_end = fish_group.span()
            try:
                fish_id = Fish.objects.get(abbreviation=fish)
            except:
                print (fish," was not found in fish database!")  #ats not found in database
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
        
        fish_str = re.search ("\d*\.?\d", length_string)
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

        lines.append ([row, stock_date, lake_id, fish_id, genotype, strain, fish_length, number_of_fish])
    return lines

def run():
    data = get_data()
    # print (data)