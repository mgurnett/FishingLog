from django.urls import path
from . import views
from .views import (
    RegionListView,
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
]