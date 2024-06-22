from catches.models import *
from taggit.models import Tag

def master_tag_list():
    mtl = []
    lakes = Lake.objects.all()
    for lake in lakes:
        if lake.static_tag:
            mtl.append(lake.static_tag)
    fishes = Fish.objects.all()
    for fish in fishes:
        if fish.static_tag:
            mtl.append(fish.static_tag)
    flys = Fly.objects.all()
    for fly in flys:
        if fly.static_tag:
            mtl.append(fly.static_tag)
    bugs = Bug.objects.all()
    for bug in bugs:
        if bug.static_tag:
            mtl.append(bug.static_tag)
    return mtl


def run():
    big_list = master_tag_list()
    print (len(big_list))

    tags = Tag.objects.all()
    for tag in tags:

        found = False
        for t in big_list:
            if str(t) == str(tag):
                found = True
                
        if not found:
            print (f"can't find - {tag}")
        
        # post_items = post_items.filter(tags__name__icontains=query)
        # https://stackoverflow.com/questions/73093347/search-with-django-for-tags