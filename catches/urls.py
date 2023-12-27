from django.urls import path,re_path
from . import views
from .views import *
        
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
    re_path(r'^flys/new/$', FlyCreateView.as_view(), name = 'fly_create'), # this is same as normal
    #This allows to add a model name with id to set initial data.
    re_path(r'^flys/new/(?P<field>[a-z_]+)/(?P<pk>[0-9]+)/$', FlyCreateView.as_view(), name = 'fly_create'),   
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
    path ('chart/graph/<int:pk>/', views.ChartGraph.as_view(), name ="chart_graph" ),

    path ('hatch/', HatchListView.as_view(), name = 'hatch_list'), 
    path ('hatch/<int:pk>/', HatchDetailView.as_view(), name = 'hatch_detail'), 
    path ('hatch/new/', HatchCreateView.as_view(), name = 'hatch_create'),  
    path ('hatch/newl/<int:pk>/', HatchCreateView_from_lake.as_view(), name = 'hatch_create_from_lake'),
    path ('hatch/newb/<int:pk>/', HatchCreateView_from_bug.as_view(), name = 'hatch_create_from_bug'),
    path ('hatch/update/<int:pk>/', HatchUpdateView.as_view(), name = 'hatch_update'), 
    path ('hatch/delete/<int:pk>/', HatchDeleteView.as_view(), name = 'hatch_delete'),    
    
    path ('week/', WeekListView.as_view(), name = 'week_list'), 
    path ('week/<int:pk>/', WeekDetailView.as_view(), name = 'week_detail'),    
    
    path ('log/', LogListView.as_view(), name = 'log_list'), 
    path ('log/<int:pk>/', LogDetailView.as_view(), name = 'log_detail'), 
    path ('log/new/', LogCreateView.as_view(), name = 'log_create'),  
    path ('log/newl/<int:pk>/', LogCreateView_from_lake.as_view(), name = 'log_create_from_lake'),
    path ('log/newt/<int:pk>/', LogCreateView_from_temp.as_view(), name = 'log_create_from_temp'),
    path ('log/duplicate/<int:pk>/', LogDuplicateView.as_view(), name = 'log_duplicate'),
    path ('log/update/<int:pk>/', LogUpdateView.as_view(), name = 'log_update'), 
    path ('log/delete/<int:pk>/', LogDeleteView.as_view(), name = 'log_delete'),
    path ('log/search/', LogListView_search.as_view(), name = 'log_search_list'),
    path ('log/graph/', views.Graph.as_view(), name ="log_graph" ),
    
    path ('stock/', StockListView.as_view(), name = 'stock_list'), 
    path ('stock/<int:pk>/', StockDetailView.as_view(), name = 'stock_detail'), 
    path ('stock/new/', StockCreateView.as_view(), name = 'stock_create'),  
    path ('stock/update/<int:pk>/', StockUpdateView.as_view(), name = 'stock_update'), 
    path ('stock/delete/<int:pk>/', StockDeleteView.as_view(), name = 'stock_delete'),

    path ('videos/',                  views.VideoListView.as_view(),    name ="videos_list" ),
    re_path(r'^videos/new/$', VideoCreateView.as_view(), name = 'video_create'),# this is same as normal
    #This allows to add a model name with id to set initial data.
    re_path(r'^videos/new/(?P<field>[a-z_]+)/(?P<pk>[0-9]+)/(?P<tag>[A-Za-z_-]+)/$', VideoCreateView.as_view(), name = 'video_create'), 
    # path ('videos/add/',              views.VideoCreateView.as_view(),  name ="video_create" ),
    path ('videos/<int:pk>/',         views.VideoDetailView.as_view(),  name ="video_detail" ),
    path ('videos/update/<int:pk>/',  views.VideoUpdateView.as_view(),  name ='video_update'), 
    path ('videos/delete/<int:pk>/',  views.VideoDeleteView.as_view(),  name ='video_delete'),

    path ('articles/',                  views.ArticleListView.as_view(),    name ="articles_list" ),
    re_path(r'^articles/new/$', ArticleCreateView.as_view(), name = 'article_create'),# this is same as normal
    #This allows to add a model name with id to set initial data.
    re_path(r'^articles/new/(?P<field>[a-z_]+)/(?P<pk>[0-9]+)/(?P<tag>[A-Za-z_-]+)/$', ArticleCreateView.as_view(), name = 'article_create'), 
    # path ('articles/add/',              views.ArticleCreateView.as_view(),  name ="article_create" ),
    path ('articles/<int:pk>/',         views.ArticleDetailView.as_view(),  name ="article_detail" ),
    path ('articles/update/<int:pk>/',  views.ArticleUpdateView.as_view(),  name ='article_update'), 
    path ('articles/delete/<int:pk>/',  views.ArticleDeleteView.as_view(),  name ='article_delete'),
    
    path ('pictures/',                  views.PictureListView.as_view(),    name ="pictures_list" ),
    re_path(r'^pictures/new/$', PictureCreateView.as_view(), name = 'picture_create'),# this is same as normal
    #This allows to add a model name with id to set initial data.
    re_path(r'^pictures/new/(?P<field>[a-z_]+)/(?P<pk>[0-9]+)/(?P<tag>[A-Za-z_-]+)/$', PictureCreateView.as_view(), name = 'picture_create'), 
    # path ('pictures/add/',              views.PictureCreateView.as_view(),  name ="picture_create" ),
    path ('pictures/<int:pk>/',         views.PictureDetailView.as_view(),  name ="picture_detail" ),
    path ('pictures/update/<int:pk>/',  views.PictureUpdateView.as_view(),  name ='picture_update'), 
    path ('pictures/delete/<int:pk>/',  views.PictureDeleteView.as_view(),  name ='picture_delete'), 
    
    path ('tags/', views.TagsListView, name ="tags_list" ),
    path ('tags/<int:pk>/', views.TagsDetailView, name ="tag_detail" ),

    path ('search/', views.searchview, name = 'search_list'),

    path ('lakes/district/<int:pk>/', LakeListView_districts.as_view(), name = 'lake_list_dist'),

    path ('plan/<int:lpk>/<int:wpk>/', views.Plan.as_view(), name ="plan" ),
    path ('button/<int:pk>/', make_kml_file, name ='make_kml' ),
    path ('library/', views.LibraryListView.as_view(), name ="library_list" ),
    path ('library/<str:tag>/', views.LibraryDetailView.as_view(), name ="library_detail" ),

]
