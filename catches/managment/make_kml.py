from django.core.management import BaseCommand
from lakes.models import Lake as Water

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('water_ids', nargs='+', type=int)  #gets an argument

    def handle(self, *args, **options):
        # for water_id in options['water_ids']:  #uses the argument
        #     print (water_id)
        # lakes = Water.objects.filter(favourite=True)
        
        lakes = Water.objects.all()
        print ('<?xml version="1.0" encoding="UTF-8"?>')
        print ('<kml xmlns="http://www.opengis.net/kml/2.2">')
        print ('<Document>')
        for lake in lakes:
            print ('    <Placemark>')
            print (f'       <name>{lake.name}</name>')
            # print (f' <styleUrl>#icon-503-DB4436-labelson-nodesc</styleUrl>')
            print ('        <Point>')
            print (f'           <coordinates>{lake.long},{lake.lat},0</coordinates>')
            print ('        </Point>')
            print ('    </Placemark>')
        
        print ('</Document>')
        print ('</klm>')



  