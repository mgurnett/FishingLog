from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

admin.site.register(Profile)

class MyUserAdmin(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'
    list_display = ['username', 'first_name', 'last_name', 'is_active', 'group', 'last_login', 'email', ]
    # list_filter = ("first_name",  )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)