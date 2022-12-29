from catches.models import *
import csv
from django.utils import timezone

# python manage.py runscript stock_import
# python manage.py runscript stock_import --script-args staleonly
# def run(*args):

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# https://towardsdatascience.com/use-python-scripts-to-insert-csv-data-into-django-databases-72eee7c6a433



def run():
    Log.objects.all().delete()
    with open('fish stock/fish_swami_log.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        for row in reader:
            try:  # check to see if we have the lake in the database already
                lake_id = Lake.objects.get(id=row[4])
            except:
                print (f'We have a missing lake for {row[4]}')

            try:  # check to see if we have the fish in the database already
                fish_id = Fish.objects.get(id=row[6])
            except:
                print (f'We are looking for fish {row[6]} and we failed')

            try:  # check to see if we have the fish in the database already
                fly_id = Fly.objects.get(id=row[5])
            except:
                print (f'We are looking for fly {row[5]} and we failed')

            try:  # check to see if we have the fish in the database already
                temp_id = Temp.objects.get(id=row[2])
            except:
                print (f'We are looking for temp {row[2]} and we failed')
                temp_id = Temp.objects.get(id=1)

            if row[1] == "":
                colour = ""
            else:
                colour = row[1]

                
            log = Log (
                num_landed = row[0],
                temp = temp_id,
                catch_date = row[3],
                lake = lake_id,
                fly = fly_id,
                fish = fish_id,
                fish_swami = row[7],
                fly_colour = colour,
                )
            print (log)
            log.save()