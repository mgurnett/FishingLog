from django.urls import path
from . import views
from .views import (
    RegionListView,
    RegionCreateView,
    RegionUpdateView,
    RegionDetailView,
    RegionDeleteView,
    # LakeListView,
    # LakeCreateView,
    # LakeDetailView,
    # LakeUpdateView,
    # LakeDeleteView,
    # StockListView,
    # LakeListView_search,
    # LakeListView_fav,
    # RegionListView,
    # LakeListView_regions,
)
        
        
urlpatterns = [
    path ('', views.home, name = 'catch_home'),
    path ('regions/', RegionListView.as_view(), name = 'region_list'), 
    path ('regions/<int:pk>/', RegionDetailView.as_view(), name = 'region_detail'), 
    path ('regions/new/', RegionCreateView.as_view(), name = 'region_create'),  
    path ('regions/update/<int:pk>/', RegionUpdateView.as_view(), name = 'region_update'), 
    path ('regions/delete/<int:pk>/', RegionDeleteView.as_view(), name = 'region_delete')
]