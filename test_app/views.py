from django.shortcuts import render
from .models import Fly, Bug, Fly_type

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
from test_app.forms import New_Flys_Form

def home (request):
    return render (request, 'test_app/home.html', {})

class FlyListView (ListView):
    model = Fly
    context_object_name = 'flys' 
    paginate_by = 6

class FlyDetailView (DetailView): 
    model = Fly
    context_object_name = 'fly'

class FlyCreateView(LoginRequiredMixin, CreateView):
    model = Fly
    form_class = New_Flys_Form
    success_message = "New fly saved"

class FlyUpdateView(LoginRequiredMixin, UpdateView):
    model = Fly
    form_class = New_Flys_Form
    success_message = "Fly fixed"

class FlyDeleteView (LoginRequiredMixin, DeleteView):
    model = Fly
    success_url = "/flys/"
