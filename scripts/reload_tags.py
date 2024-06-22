from catches.models import *
from taggit.models import Tag

def run():
    pictures = Picture.objects.using("sqlite").all()
    
    for picture in pictures:
        print (f'sqlite - {picture.name = } - {picture.id = } - {picture.tags= }')
        # for tag in picture.tag_list:
        #     print (f'{tag = }')
    
    all_tags = Tag.objects.all().order_by('name')
    
    for tag in all_tags:
        print (f'sqlite - {tag.name = } - {tag.id = }')
        # for tag in picture.tag_list:
        #     print (f'{tag = }')




    # pictures = Picture.objects.using("default").all()
    
    # for picture in pictures:
    #     print (f'mysql - {picture.name = }')
    #     for tag in picture.tag_list:
    #         print (f'{tag = }')
