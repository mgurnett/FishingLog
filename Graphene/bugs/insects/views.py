from django.shortcuts import render
from django.views.generic.base import TemplateView

def home (request):
    return render (request, 'insects/home.html', {})