from django.urls import path,re_path
from . import views
from .views import *
from .scaffolding import *
bug_crud = BugCrudManager()
temp_crud = TempCrudManager()
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from insects.schema import schema
        
urlpatterns = [
    path ('', views.home, name = 'catch_home'),

    # path ('regions/', RegionListView.as_view(), name = 'region_list'), 
    # path ('regions/<int:pk>/', RegionDetailView.as_view(), name = 'region_detail'), 
    # path ('regions/new/', RegionCreateView.as_view(), name = 'region_create'),  
    # path ('regions/update/<int:pk>/', RegionUpdateView.as_view(), name = 'region_update'), 
    # path ('regions/delete/<int:pk>/', RegionDeleteView.as_view(), name = 'region_delete'),

    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

urlpatterns += bug_crud.get_url_patterns()
urlpatterns += temp_crud.get_url_patterns()