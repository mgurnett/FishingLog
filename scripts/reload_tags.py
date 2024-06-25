from catches.models import *
from taggit.models import Tag
import csv

def get_sqlite_data (model, id):
    if model == "picture":
        model_object = Picture.objects.using("sqlite").get(id=id)
    return model_object

def get_tag_info (id):
    return Tag.get(id=id)

    
    # This gets all the tag names
    # all_tags = Tag.objects.all().order_by('name')
    
    # for tag in all_tags:
    #     print (f'sqlite - {tag.name = } - {tag.id = }')


def run():
    with open('taggit-a.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        for row in reader:
            print (f'working on {row[1] = }')
            article = Article.objects.get (id=row[1])
            tag= Tag.objects.get (id=row[3]).name
            article.tags.add (tag)
            print (f'{article.id = } worked')
    # print (f'{picture = }')
    # picture.save()

    # pictures = Picture.objects.all()

    # for picture in pictures:
    #     print (f'MariaDB - {picture.name = } - {picture.id = }')
    #     for tag in picture.tag_list:
    #         print (f'{tag = }')

    #     sqlite_picture = get_sqlite_data ("picture", picture.id)
    #     print (f'Sqlite - {sqlite_picture.name = } - {sqlite_picture.id = }')
    #     print (f'Sqlite - {sqlite_picture.tags.all = }')
    #     for tag in sqlite_picture.tags.all:
    #         print (f'{tag = }')


    # tag_itme = Tagged_item
