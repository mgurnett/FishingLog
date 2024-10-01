from catches.models import *

dists = [30]
fish_icon = 1573
yellow = "FBC02D"
blue = "0097A7"
green ="0F9D58"

def run():
    with open('Norhtern Alberta Lakes30.kml', 'w') as f:
        start_line = (f"""         
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Norhtern Alberta Lakes30.kml</name> """)   
        f.write(start_line)     
        lakes = Lake.objects.all ()      
        for id, lake in enumerate (lakes):
            line = (f"""         
        <Placemark>
            <name>{lake.name}</name>
            <description>{lake.other_name}</description>
            <Point>
                <coordinates>
                    {lake.long},{lake.lat},0
                </coordinates>
            </Point>
        </Placemark>""")
                    
            # print (line)
            if lake.district in dists:
                f.write(line)
        end_line = (f"""         
    </Document>
</kml>""") 
        f.write(end_line)
        # print (prov)


'''    
    class Lake(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField (blank=True, null=True)
    fish = models.ManyToManyField (Fish, through='Stock', blank=True)
    other_name = models.CharField (max_length=100, blank=True)
    ats = models.CharField (max_length=100, blank=True)
    lat = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    long = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    # district = models.CharField (max_length=100, blank=True, choices = DISTRICTS)
    district = models.IntegerField (blank=True, null=True)
    waterbody_id = models.IntegerField (blank=True, null=True)
    # favourite = models.BooleanField (default = False)
    static_tag = models.SlugField() 
    gps_url = models.URLField(max_length = 200, blank=True)
'''
