from catches.models import *



def run():
    old=""
    lakes = Lake.objects.all()
    for lake in lakes:
        name = lake.name
        slug = slugify (name)
        lake.static_tag = f"lake,{slug}"
        print (lake.static_tag)
