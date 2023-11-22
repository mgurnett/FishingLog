# importing googlemaps module
import googlemaps
# https://python-gmaps.readthedocs.io/en/latest/gmaps.html#gmaps.directions.Directions.directions
# Requires API key

def find_dist (lake):
    gmaps = googlemaps.Client(key='AIzaSyB-oms0UbhKCb8Cla7_M64Zq54BO8p5LOo')

    # Requires cities name
    # my_dist = gmaps.distance_matrix('Calgary, AB','Edmonton, AB')
    # my_dist = gmaps.distance_matrix('11940 52St NW, Edmonton, AB','53.6832190000, -113.2741360000')
    my_dist = gmaps.distance_matrix('11940 52St NW, Edmonton, AB', str (lake.lat) + "," + str (lake.long) )
    my_dist_dict = { 
        'distance_text': my_dist['rows'][0]['elements'][0]['distance']['text'],
        'meters': my_dist['rows'][0]['elements'][0]['distance']['value'],
        'time_text': my_dist['rows'][0]['elements'][0]['duration']['text'],
        'minutes': my_dist['rows'][0]['elements'][0]['duration']['value'],
    }
    return (my_dist_dict)




if __name__ == "__main__":
    Lat = 53.6832190000
    Lon = -113.2741360000
    distance = find_dist (Lat, Lon)
    # Printing the result
    print(distance['rows'][0]['elements'][0]['distance']['text'])
    print(distance['rows'][0]['elements'][0]['duration']['text'])