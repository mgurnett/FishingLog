from catches.models import Lake
from django.template.defaultfilters import slugify

def add_tag (lake):
    print (f'tag saved for: {lake = }')
    lake.static_tag = slugify(lake.name)
    lake.save()

def run():
    lakes = Lake.objects.all()
    
    for lake in lakes:
        if not lake.static_tag:
            # print (f'tag missing for: {lake = }')
            add_tag (lake)