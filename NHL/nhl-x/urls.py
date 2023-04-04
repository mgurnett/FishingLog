from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('team/<int:pk>/', views.Team.as_view(), name='team'),
]