from django.core.management import BaseCommand
from lakes.models import Lake, Region

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        lakes = Lake.objects.all()
        regions = Region.objects.all()
        for lake in lakes:
            if lake.region:
                if not lake.region in regions: # if true, we want to add this to the database via model.Region
                    regions.append(lake.region)




#  to run python3 manage.py regions