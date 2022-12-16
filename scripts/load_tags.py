from catches.models import Lake

def run():
    lakes = Lake.objects.all()
    
    for lake in lakes:
        print (lake)
        lake.tag_name = "lake"
        lake.save()

