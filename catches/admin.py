from django.contrib import admin
from .models import *
from catches.helpers.fish_data import *

# admin.site.register (Lake)
# admin.site.register (Stock)
# admin.site.register (Region)
admin.site.register (Fish)
# admin.site.register (Fly)
admin.site.register (Bug)
# admin.site.register (Log)
admin.site.register (Hatch)
admin.site.register (Chart)
# admin.site.register (Week)
admin.site.register (Fly_type)


@admin.register (Stock)
class StockAdmin (admin.ModelAdmin):
    list_display = ['date_stocked', 'lake', 'fish', 'number', 'length', 'strain', 'gentotype']

@admin.register (Video)
class VideoAdmin (admin.ModelAdmin):
    list_display = ['name', 'get_tags', 'url']

    def get_tags (self, obj):
        return ", ".join(o for o in obj.tags.names())

@admin.register (Article)
class ArticleAdmin (admin.ModelAdmin):
    list_display = ['name', 'get_tags']

    def get_tags (self, obj):
        return ", ".join(o for o in obj.tags.names())

@admin.register (Picture)
class PictureAdmin (admin.ModelAdmin):
    list_display = ['name', "image", 'get_tags']

    def get_tags (self, obj):
        return ", ".join(o for o in obj.tags.names())

@admin.register (Fly)
class FlyAdmin (admin.ModelAdmin):
    list_display = ['name', 'static_tag']

@admin.register (Temp)
class TempAdmin (admin.ModelAdmin):
    list_display = ['name', 'notes', 'deg', 'direction', 'search_keys']

@admin.register (Log)
class LogAdmin (admin.ModelAdmin):
    list_display = ['catch_date', 'lake', 'fish', 'temp', 'week', 'angler']

@admin.register (Lake)
class LakeAdmin (admin.ModelAdmin):
    list_display = ['name', 'landl', 'static_tag', 'dist_name', 'reg_location']

    def landl (self, obj):
        return str(f'{obj.lat:.5f} & {obj.long:.5f}')

    def dist_name (self, obj):
        dis = int(obj.district)
        dis_name = DISTRICTS[dis][1]
        print (f'{dis = } & {dis_name = }')
        return str(f'{dis_name}')

@admin.register (Region)
class RegionAdmin (admin.ModelAdmin):
    list_display = ['name', 'profile']

@admin.register (Favorite)
class FavoriteAdmin (admin.ModelAdmin):
    list_display = ['lake', 'user']

@admin.register (Announcment)
class AnnouncmentAdmin (admin.ModelAdmin):
    list_display = ['notes', 'lake_id']


@admin.register (Week)
class WeekAdmin (admin.ModelAdmin):
    list_display = ['number', 'ave_temp']