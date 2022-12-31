from django.core.management import BaseCommand
from models import Lake, Region
import simplekml

class Command(BaseCommand):

    def get_context_data(self, **kwargs):
        context = super(Command, self).get_context_data(**kwargs)
        region_id=self.kwargs['pk']
        lakes = Lake.objects.filter (region=region_id)
        region_name = Region.objects.get(pk=region_id).name

        kml = simplekml.Kml()

        for lake in lakes:
            kml.newpoint(
                name = lake.lake_info, 
                description = lake.region,
                coords=[(lake.long,lake.lat)]
            )  # lon, lat optional height

            file_name = f'media/{region_name}.kml'

        kml.save(file_name)



  