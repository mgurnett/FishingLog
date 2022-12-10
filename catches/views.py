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
from catches.forms import *

def home (request):
    return render (request, 'catches/home.html', {})

class RegionListView (ListView):
    model = Region
    context_object_name = 'regions' 
    paginate_by = 6

class RegionDetailView (DetailView): 
    model = Region
    context_object_name = 'region'

class RegionCreateView(LoginRequiredMixin, CreateView):
    model = Region
    form_class = New_Regions_Form
    success_message = "New region saved"

class RegionUpdateView(LoginRequiredMixin, UpdateView):
    model = Region
    form_class = New_Regions_Form
    success_message = "Region fixed"

class RegionDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Region
    success_url = "/regions/"

class Fly_typeListView (ListView):
    model = Fly_type
    context_object_name = 'fly_types' 
    paginate_by = 6

class Fly_typeDetailView (DetailView): 
    model = Fly_type
    context_object_name = 'fly_type'

class Fly_typeCreateView(LoginRequiredMixin, CreateView):
    model = Fly_type
    form_class = New_Fly_type_Form
    success_message = "New Fly type saved"

class Fly_typeUpdateView(LoginRequiredMixin, UpdateView):
    model = Fly_type
    form_class = New_Fly_type_Form
    success_message = "Fly type fixed"

class Fly_typeDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Region
    success_url = "/regions/"

class FishListView (ListView):
    model = Fish
    context_object_name = 'fishes' 
    paginate_by = 6

class FishDetailView (DetailView): 
    model = Fish
    context_object_name = 'fishes'

class FishCreateView(LoginRequiredMixin, CreateView):
    model = Fish
    form_class = New_Fish_Form
    success_message = "New Fish saved"

class FishUpdateView(LoginRequiredMixin, UpdateView):
    model = Fish
    form_class = New_Fish_Form
    success_message = "Fish fixed"

class FishDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Fish
    success_url = "/fish/"

class BugListView (ListView):
    model = Bug
    context_object_name = 'bugs' 
    paginate_by = 6

class BugDetailView (DetailView): 
    model = Bug
    context_object_name = 'bug'

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    form_class = New_Bug_Form
    success_message = "New Bug saved"

class BugUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    form_class = New_Bug_Form
    success_message = "Bug fixed"

class BugDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Bug
    success_url = "/bug/"

class FlyListView (ListView):
    model = Fly
    context_object_name = 'flys' 
    paginate_by = 6

class FlyDetailView (DetailView): 
    model = Fly
    context_object_name = 'fly'

class FlyCreateView(LoginRequiredMixin, CreateView):
    model = Fly
    form_class = New_Fly_Form
    success_message = "New Fly saved"

class FlyUpdateView(LoginRequiredMixin, UpdateView):
    model = Fly
    form_class = New_Fly_Form
    success_message = "Fly fixed"

class FlyDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Fly
    success_url = "/fly/"

class LakeListView (ListView):
    model = Lake
    context_object_name = 'lakes' 
    paginate_by = 6

class LakeDetailView (DetailView): 
    model = Lake
    context_object_name = 'lake'

class LakeCreateView(LoginRequiredMixin, CreateView):
    model = Lake
    form_class = New_Lake_Form
    success_message = "New Lake saved"

class LakeUpdateView(LoginRequiredMixin, UpdateView):
    model = Lake
    form_class = New_Lake_Form
    success_message = "Lake fixed"

class LakeDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Lake
    success_url = "/lake/"

class TempListView (ListView):
    model = Temp
    context_object_name = 'temps' 
    paginate_by = 6

class TempDetailView (DetailView): 
    model = Temp
    context_object_name = 'temp'

class TempCreateView(LoginRequiredMixin, CreateView):
    model = Temp
    form_class = New_Temp_Form
    success_message = "New Temp saved"

class TempUpdateView(LoginRequiredMixin, UpdateView):
    model = Temp
    form_class = New_Temp_Form
    success_message = "Temp fixed"

class TempDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Temp
    success_url = "/temp/"

class Bug_siteListView (ListView):
    model = Bug_site
    context_object_name = 'bug_sites' 
    paginate_by = 6

class Bug_siteDetailView (DetailView): 
    model = Bug_site
    context_object_name = 'bug_site'

class Bug_siteCreateView(LoginRequiredMixin, CreateView):
    model = Bug_site
    form_class = New_Bug_site_Form
    success_message = "New Bug_site saved"

class Bug_siteUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug_site
    form_class = New_Bug_site_Form
    success_message = "Bug_site fixed"

class Bug_siteDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Bug_site
    success_url = "/bug_site/"

class LogListView (ListView):
    model = Log
    context_object_name = 'logs' 
    paginate_by = 6

class LogDetailView (DetailView): 
    model = Log
    context_object_name = 'log'

class LogCreateView(LoginRequiredMixin, CreateView):
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

class LogUpdateView(LoginRequiredMixin, UpdateView):
    model = Log
    form_class = New_Log_Form
    success_message = "Log fixed"

class LogDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Log
    success_url = "/log/"

class StockListView (ListView):
    model = Stock
    context_object_name = 'stocks' 
    paginate_by = 6

class StockDetailView (DetailView): 
    model = Stock
    context_object_name = 'stock'

class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = New_Stock_Form
    success_message = "New Stock saved"

class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = New_Stock_Form
    success_message = "Stock fixed"

class StockDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Stock
    success_url = "/stock/"