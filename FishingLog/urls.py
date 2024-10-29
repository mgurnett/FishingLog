from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.urls import re_path
from django.views.static import serve
from django.urls import path, include,re_path
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view( template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='users/password_reset_confirm.html' ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view( template_name='users/password_reset_complete.html' ), name='password_reset_complete'),
    path ('', include ('catches.urls')),
    path ('blog/', include ('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
	re_path(r'^uploads/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]

from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = 'FishingLog administration'              # default: "Django Administration"
admin.site.index_title = 'Welcome to the FishingLog admin area'   # default: "Site administration"  browser title
admin.site.site_title = 'FishingLog admin'                        # default: "Django site admin"