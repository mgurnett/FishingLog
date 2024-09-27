from catches.models import *

def run():
    lakes = Lake.objects.all ()
    file_name = f'Alberta Lakes.kml'   
    prov = []     
    for id, lake in enumerate (lakes):
        line = str(f'         <Placemark id="{id}">', end="\r")
                #         <Placemark id="{id}">
                #             <name>{lake.name}</name>
                #             <description>{lake.other_name}</description>
                #             <point>
                #                 <coordinates>{lake.lat},{lake.long},0.0</coordinates>
                #             </point>
                #         </Placemark>
                # ')
                
        prov.append (line)
    print (prov)


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
