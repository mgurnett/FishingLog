from insects.models import *

def run():
    temps = Temp.objects.all()

    for t in temps:
        print (t)