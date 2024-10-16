from django.contrib import admin
from .models import *

# admin.site.register (Lake)
admin.site.register (Stock)
# admin.site.register (Region)
admin.site.register (Fish)
# admin.site.register (Fly)
admin.site.register (Bug)
# admin.site.register (Log)
admin.site.register (Hatch)
admin.site.register (Chart)
admin.site.register (Week)
admin.site.register (Fly_type)

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
    list_display = ['name', 'get_tags']

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
    list_display = ['catch_date', 'lake', 'fish', 'temp', 'week']

@admin.register (Lake)
class LakeAdmin (admin.ModelAdmin):
    list_display = ['name', 'lat', 'long', 'static_tag','district','reg_location']

@admin.register (Region)
class RegionAdmin (admin.ModelAdmin):
    list_display = ['name', 'profile']

@admin.register (Favorite)
class FavoriteAdmin (admin.ModelAdmin):
    list_display = ['lake', 'user']

@admin.register (Announcment)
class AnnouncmentAdmin (admin.ModelAdmin):
    list_display = ['notes', 'lake_id']