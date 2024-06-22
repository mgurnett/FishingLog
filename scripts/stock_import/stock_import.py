from catches.models import *
import csv

# python manage.py runscript stock_import
# python manage.py runscript stock_import --script-args staleonly
# def run(*args):

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# https://towardsdatascience.com/use-python-scripts-to-insert-csv-data-into-django-databases-72eee7c6a433

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
    ('Marie Creek', 'MC'),
    ('Rock Island', 'RI'),
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
    ("MC", 'Marie Creek'),
    ("RI", 'Rock Island'),
)

GENTOTYPE = (
    ("2N", "diploid"),
    ("3N", "triploid"),
    ("AF2N", "all-female diploid"),
    ("AF3N", "all-female triploid"),
)

def run():
    with open('static/stock_reports/epa-alberta-fish-stocking-report-2023.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        # Stock.objects.all().delete()

        for stock_count, row in enumerate(reader):
            # print (row)
            try:  # check to see if we have the lake in the database already
                lake_id = Lake.objects.get(ats=row[2])
                # print (lake_id)
            except:
                print (f'We have a missing lake for {row[0]} ({row[1]})')

            try:  # check to see if we have the fish in the database already
                fish_id = Fish.objects.get(abbreviation=row[3])
            except:
                print (f'We are looking for {row[3]} and we failed')

            found=0
            strain = ""
            for index, str_look in enumerate(STRAIN_lookup):
                if row[4] == str_look[0]:
                    found=index
            if found == 0:
                print (f'We are going to look for {row[4]} in lake {lake_id} with fish {fish_id}')
            else:
                strain = STRAIN_lookup[found][1]

            if row[5] in ("2N", "3N", "AF2N", "AF3N"):
                geo = row[5]
            else:
                geo = ""
            
            stock = Stock (
                date_stocked = row[8],
                number = row[7],
                length = row[6],
                lake = lake_id,
                fish = fish_id,
                strain = strain,
                gentotype = geo,
                )
            print (f'{stock_count+2} - {stock}')
            stock.save()

    # print (all_stock.order_by(date_stocked))
    # lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    # fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    # date_stocked = models.DateField()
    # number = models.IntegerField ()
    # length = models.DecimalField (max_digits = 10, decimal_places=2)
    # strain = models.CharField ()

    # Stocking Date,Waterbody ID,Water Type,Waterbody Official Name,Waterbody Common Name,District,Latitude,Longitude,
    # Waterbody ATS,Species Code,Species Common Name,Number,Average Length,Average Weight,Genotype,Strain,Station