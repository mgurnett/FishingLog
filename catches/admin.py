from django.contrib import admin
from .models import *

admin.site.register (Lake)
admin.site.register (Stock)
admin.site.register (Region)
admin.site.register (Fish)
admin.site.register (Fly)
admin.site.register (Bug)
admin.site.register (Log)
admin.site.register (Bug_site)
admin.site.register (Fly_type)
admin.site.register (Hatch)
admin.site.register (Week)
admin.site.register (Strength)

@admin.register (Video)
class VideoAdmin (admin.ModelAdmin):
    list_display = ['name', 'get_tags']

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

@admin.register (Temp)
class TempAdmin (admin.ModelAdmin):
    list_display = ['name', 'deg', 'direction', 'search_keys']