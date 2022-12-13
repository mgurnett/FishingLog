from django.urls import path
from . import views
from .views import (
    RegionListView, RegionCreateView, RegionUpdateView, RegionDetailView, RegionDeleteView,
    Fly_typeListView, Fly_typeCreateView, Fly_typeUpdateView, Fly_typeDetailView, Fly_typeDeleteView,
    FishListView, FishCreateView, FishUpdateView, FishDetailView, FishDeleteView,
    BugListView, BugCreateView, BugUpdateView, BugDetailView, BugDeleteView,    
    FlyListView, FlyCreateView, FlyUpdateView, FlyDetailView, FlyDeleteView,
    LakeListView, LakeCreateView, LakeUpdateView, LakeDetailView, LakeDeleteView,
    TempListView, TempCreateView, TempUpdateView, TempDetailView, TempDeleteView,
    Bug_siteListView, Bug_siteCreateView, Bug_siteUpdateView, Bug_siteDetailView, Bug_siteDeleteView,
    LogListView, LogCreateView, LogUpdateView, LogDetailView, LogDeleteView,
    StockListView, StockCreateView, StockUpdateView, StockDetailView, StockDeleteView,
    LakeListView_search, LogListView_search, LakeListView_regions, LakeListView_fav
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
    
    path ('fish/', FishListView.as_view(), name = 'fish_list'), 
    path ('fish/<int:pk>/', FishDetailView.as_view(), name = 'fish_detail'), 
    path ('fish/new/', FishCreateView.as_view(), name = 'fish_create'),  
    path ('fish/update/<int:pk>/', FishUpdateView.as_view(), name = 'fish_update'), 
    path ('fish/delete/<int:pk>/', FishDeleteView.as_view(), name = 'fish_delete'),
    
    path ('bug/', BugListView.as_view(), name = 'bug_list'), 
    path ('bug/<int:pk>/', BugDetailView.as_view(), name = 'bug_detail'), 
    path ('bug/new/', BugCreateView.as_view(), name = 'bug_create'),  
    path ('bug/update/<int:pk>/', BugUpdateView.as_view(), name = 'bug_update'), 
    path ('bug/delete/<int:pk>/', BugDeleteView.as_view(), name = 'bug_delete'),    
    
    path ('flys/', FlyListView.as_view(), name = 'fly_list'), 
    path ('flys/<int:pk>/', FlyDetailView.as_view(), name = 'fly_detail'), 
    path ('flys/new/', FlyCreateView.as_view(), name = 'fly_create'),  
    path ('flys/update/<int:pk>/', FlyUpdateView.as_view(), name = 'fly_update'), 
    path ('flys/delete/<int:pk>/', FlyDeleteView.as_view(), name = 'fly_delete'),    
    
    path ('lakes/', LakeListView.as_view(), name = 'lake_list'), 
    path ('lakes/<int:pk>/', LakeDetailView.as_view(), name = 'lake_detail'), 
    path ('lakes/new/', LakeCreateView.as_view(), name = 'lake_create'),  
    path ('lakes/update/<int:pk>/', LakeUpdateView.as_view(), name = 'lake_update'), 
    path ('lakes/delete/<int:pk>/', LakeDeleteView.as_view(), name = 'lake_delete'),      
    
    path ('temp/', TempListView.as_view(), name = 'temp_list'), 
    path ('temp/<int:pk>/', TempDetailView.as_view(), name = 'temp_detail'), 
    path ('temp/new/', TempCreateView.as_view(), name = 'temp_create'),  
    path ('temp/update/<int:pk>/', TempUpdateView.as_view(), name = 'temp_update'), 
    path ('temp/delete/<int:pk>/', TempDeleteView.as_view(), name = 'temp_delete'),

    path ('bug_site/', Bug_siteListView.as_view(), name = 'bug_site_list'), 
    path ('bug_site/<int:pk>/', Bug_siteDetailView.as_view(), name = 'bug_site_detail'), 
    path ('bug_site/new/', Bug_siteCreateView.as_view(), name = 'bug_site_create'),  
    path ('bug_site/update/<int:pk>/', Bug_siteUpdateView.as_view(), name = 'bug_site_update'), 
    path ('bug_site/delete/<int:pk>/', Bug_siteDeleteView.as_view(), name = 'bug_site_delete'),    
    
    path ('log/', LogListView.as_view(), name = 'log_list'), 
    path ('log/<int:pk>/', LogDetailView.as_view(), name = 'log_detail'), 
    path ('log/new/', LogCreateView.as_view(), name = 'log_create'),  
    path ('log/update/<int:pk>/', LogUpdateView.as_view(), name = 'log_update'), 
    path ('log/delete/<int:pk>/', LogDeleteView.as_view(), name = 'log_delete'),
    path ('log/search/', LogListView_search.as_view(), name = 'log_search_list'),
    
    path ('stock/', StockListView.as_view(), name = 'stock_list'), 
    path ('stock/<int:pk>/', StockDetailView.as_view(), name = 'stock_detail'), 
    path ('stock/new/', StockCreateView.as_view(), name = 'stock_create'),  
    path ('stock/update/<int:pk>/', StockUpdateView.as_view(), name = 'stock_update'), 
    path ('stock/delete/<int:pk>/', StockDeleteView.as_view(), name = 'stock_delete'),

    path ('search/', LakeListView_search.as_view(), name = 'search_list'),
    path ('lakes/region/<int:pk>/', LakeListView_regions.as_view(), name = 'lake_list_reg'),
    path ('favourite/<str:favourite>/', LakeListView_fav.as_view(), name = 'lake_list_fav'),
]