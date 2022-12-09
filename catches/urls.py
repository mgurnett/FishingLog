from django.urls import path
from . import views
        
        
urlpatterns = [
    path ('', views.home, name = 'catch_home') 
]