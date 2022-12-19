from django.urls import path
from . import views
from test_app.views import (   
    FlyListView, FlyCreateView, FlyUpdateView, FlyDetailView, FlyDeleteView,
)
        
urlpatterns = [
    path ('', views.home, name = 'test_home'),

    path ('fly/', FlyListView.as_view(), name = 'afly_list'), 
    path ('flys/<int:pk>/', FlyDetailView.as_view(), name = 'afly_detail'), 
    path ('flys/new/', FlyCreateView.as_view(), name = 'afly_create'),  
    path ('flys/update/<int:pk>/', FlyUpdateView.as_view(), name = 'afly_update'), 
    path ('flys/delete/<int:pk>/', FlyDeleteView.as_view(), name = 'afly_delete'),  
    ]