from catches.models import *
import re

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

with open('static/stock_reports/2022_raw.txt') as file:
    file_contents = file.read()

lines = []
new_end = 0
for x in re.finditer ('[0-9][-][A-Z][a-z][a-z]-22', file_contents):  #find where the line ends as the date is aways the end
    start, end = x.span()
    row = str(file_contents[new_end:end]) #get the whole row

    location = re.search ('[NS][EW](\d{1,2})-(\d+)-(\d{1,2})-W[0-9]', row)  #search for the ATS
    if location:
        try:
            lake_id = Lake.objects.get(ats=location.group())
        except:
            print (location.group()," was not found lake database!")  #ats not found in database
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

    strain = str(row[fish_end:geno_start])

    found=0
    strain_short = ""
    for index, str_look in enumerate(STRAIN_lookup):
        if strain == str_look[0]:
            found=index
    if found == 0:
        # print (f'We are going to look for {strain} in lake {lake_id} with fish {fish_id}')
        pass
    else:
        strain_short = STRAIN_lookup[found][1]
        print ('found one')
    # print (row, "  ", fish_end, "  ", geno_start, "  ", strain_short)



    new_end = end + 1 #get set to read the next row

    lines.append ([row, lake_id, fish_id, genotype])
# print (lines)