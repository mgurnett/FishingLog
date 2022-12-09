from django.shortcuts import render
from .models import *

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin   # this is how we limit not allowing non-logged in users from entering a lake
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def home (request):
    return render (request, 'catches/home.html', {})

class RegionListView (ListView):
    model = Region
    context_object_name = 'regions' # this is the name that we are passing to the template
    paginate_by = 10
