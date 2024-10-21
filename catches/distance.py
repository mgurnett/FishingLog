# importing googlemaps module
import googlemaps
import simplekml
from .models import *
from django.conf import settings
from django.http import HttpResponse, FileResponse
# https://python-gmaps.readthedocs.io/en/latest/gmaps.html#gmaps.directions.Directions.directions
# Requires API key
# Tea lakes does not work in google maps either.  I need to be able to deal with this.
def find_dist (lake, user):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    address_str = f"{user.profile.address}, {user.profile.city}, {user.profile.prov}"

    # Requires cities name 
    # my_dist = gmaps.distance_matrix('Calgary, AB','Edmonton, AB')
    # my_dist = gmaps.distance_matrix('11940 52St NW, Edmonton, AB','53.6832190000, -113.2741360000')
    # my_dist = gmaps.distance_matrix('11940 52St NW, Edmonton, AB', str (lake.lat) + "," + str (lake.long) )
    my_dist = gmaps.distance_matrix(address_str, str (lake.lat) + "," + str (lake.long) )
    if my_dist['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        my_dist_dict = { 'distance_text': 'Distance not available' }
    else:
        my_dist_dict = { 
            'distance_text': my_dist['rows'][0]['elements'][0]['distance']['text'],
            'meters': my_dist['rows'][0]['elements'][0]['distance']['value'],
            'time_text': my_dist['rows'][0]['elements'][0]['duration']['text'],
            'minutes': my_dist['rows'][0]['elements'][0]['duration']['value'],
        }
    return (my_dist_dict)

def make_kml_file (request, *args, **kwargs):
    # print (kwargs)  {'pk': '8', 'model': 'R'}
    id = kwargs['pk']
    model = kwargs['model']
    # print (f"model = {model} and id is {id}")
    if model == "R":
        lakes = Lake.objects.filter (region=id)
        file_name = f'{Region.objects.get(pk=id).name}.kml'
    if model == "D":
        lakes = Lake.objects.filter (district=id)
        file_name = f'{DISTRICTS[int(id)][1]}.kml'        
    kml = simplekml.Kml()
    for lake in lakes:
        kml.newpoint(
            name = lake.name, 
            description = lake.lake_info,
            coords = [(lake.long,lake.lat)],
            # atomlink = str(f'www.ontheflys.com/lakes/{lake.id}/')
        )
    response = HttpResponse(kml.kml())
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def kml_help(request):
    # return FileResponse("How to use the kml file.pdf", as_attachment=True, filename="How to use the kml file.pdf")        
    response = FileResponse("How to use the kml file.pdf", 
                            as_attachment=True, 
                            filename='How to use the kml file.pdf')
    return response

if __name__ == "__main__":
    Lat = 53.6832190000
    Lon = -113.2741360000
    distance = find_dist (Lat, Lon)
    # Printing the result
    print(distance['rows'][0]['elements'][0]['distance']['text'])
    print(distance['rows'][0]['elements'][0]['duration']['text'])