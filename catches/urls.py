from django.urls import path
from . import views
from .views import (
    RegionListView, RegionCreateView, RegionUpdateView, RegionDetailView, RegionDeleteView,
    Fly_typeListView, Fly_typeCreateView, Fly_typeUpdateView, Fly_typeDetailView, Fly_typeDeleteView,
)
        
        
urlpatterns = [
    path ('', views.home, name = 'catch_home'),

    path ('regions/', RegionListView.as_view(), name = 'region_list'), 
    path ('regions/<int:pk>/', RegionDetailView.as_view(), name = 'region_detail'), 
    path ('regions/new/', RegionCreateView.as_view(), name = 'region_create'),  
    path ('regions/update/<int:pk>/', RegionUpdateView.as_view(), name = 'region_update'), 
    path ('regions/delete/<int:pk>/', RegionDeleteView.as_view(), name = 'region_delete'),
    
    path ('fly_type/', Fly_typeListView.as_view(), name = 'fly_type_list'), 
    path ('fly_type/<int:pk>/', Fly_typeDetailView.as_view(), name = 'fly_type_detail'), 
    path ('fly_type/new/', Fly_typeCreateView.as_view(), name = 'fly_type_create'),  
    path ('fly_type/update/<int:pk>/', Fly_typeUpdateView.as_view(), name = 'fly_type_update'), 
    path ('fly_type/delete/<int:pk>/', Fly_typeDeleteView.as_view(), name = 'fly_type_delete'),
]