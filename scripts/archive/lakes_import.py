from catches.models import *
import csv

# python manage.py runscript lakes_import
# python manage.py runscript lakes_import --script-args staleonly
# def run(*args):

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# https://towardsdatascience.com/use-python-scripts-to-insert-csv-data-into-django-databases-72eee7c6a433

def run():
     with open('fish stock/lakes.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Lake.objects.all().delete()
    
        for row in reader:
            lat_temp = row[3]
            if lat_temp == "":
                lat_temp = 0.0
            long_temp = row[4]
            if long_temp == "":
                long_temp = 0.0
            wb_id_temp = row[6]
            if wb_id_temp == "":
                wb_id_temp = 0


            lake = Lake (
                name = row[0].title(),
                other_name = row[1].title(),
                ats = row[5],
                lat = lat_temp,
                long = long_temp,
                district = row[2].title(),
                waterbody_id = wb_id_temp,
            )
            print (lake)
            lake.save()