from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.core.management import BaseCommand
from taggit.models import Tag
import pandas as pd
import plotly.express as px
import simplekml

from catches.num_array import get_array

from django.db.models import Q
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin   # this is how we limit not allowing non-logged in users from entering a lake
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from catches.forms import *
from .weather_stuff import *
from .distance import *

class UserAccessMixin (PermissionRequiredMixin):
    def dispatch (self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login (
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name()
            )
        if not self.has_permission():
            return redirect('home/')
        return super(UserAccessMixin, self).dispatch (request, *args, **kwargs)


def collect_tw_from_logs_and_hatches():
    logs = Log.objects.all()
    hatches = Hatch.objects.all()
    data = []
    for log in logs:
        if log.temp.id > 1:
            log_data = {
                'week': log.week.number, 
                'week_id': log.week.id, 
                'date': log.catch_date, 
                'temp': log.temp.deg,
                'temp_id': log.temp.id, 
                'temp_name': log.temp.name, 
                'log': log.id,
                'type': 'L'
                }
            data.append(log_data)

    for hatch in hatches:
        if hatch.temp:
            if hatch.temp.id > 1:
                log_data = {
                    'week': hatch.week.number, 
                    'week_id': hatch.week.id, 
                    'date': hatch.sight_date, 
                    'temp': hatch.temp.deg,
                    'temp_id': hatch.temp.id, 
                    'temp_name': hatch.temp.name, 
                    'log': hatch.id,
                    'type': 'H'
                    }
                data.append(log_data)
    return data  #  list of dictionaries

def get_query_set(pk): # get the data for the hatch trends for week detail view

    try:
        week_data = Week.objects.get(id=pk)
    except:
        allcharts = []
        return allcharts

    last_week = week_data.prev_num
    next_week = week_data.next_num
    
    chart_now = Chart.objects.filter (week=week_data.id)
    chart_last = Chart.objects.filter (week=last_week)
    chart_next = Chart.objects.filter (week=next_week)
    
    three_charts = []
    for index, c in enumerate(chart_now):
        if chart_last[index].strength + c.strength < c.strength + chart_next[index].strength:
            trend = "rising"
        elif chart_last[index].strength + c.strength == c.strength + chart_next[index].strength:
            trend = "flat"
        elif chart_last[index].strength + c.strength > c.strength + chart_next[index].strength:
            trend = "falling"
        insect = {
                    'bug': c.bug.name, 
                    'bug_id': c.bug.id,
                    'last': chart_last[index].strength_name, 
                    'this': c.strength_name,
                    'next': chart_next[index].strength_name,
                    'trend': trend,
                    'strength': c.strength
                }

        three_charts.append(insect)
    allcharts = sorted(three_charts, key=lambda d: d['strength'], reverse=True)
    allcharts = sorted(allcharts, key=lambda d: d['trend'], reverse=True)

    return allcharts

def get_temps(pk):
    all_temps = collect_tw_from_logs_and_hatches()
    temps_this_week = []
    for temp in all_temps:
        if temp.get("week_id") == pk:
            temps_this_week.append(temp)
    temp_list = sorted (temps_this_week, key=lambda d: d['temp_name'], reverse=True)
    return temp_list

def get_weeks(pk):
    all_weeks = collect_tw_from_logs_and_hatches()
    weeks_this_temp = []
    for week in all_weeks:
        if week.get("temp_id") == pk:
            weeks_this_temp.append(week)
    week_list = sorted (weeks_this_temp, key=lambda d: d['week'], reverse=True)
    return week_list

def make_kml_file (request, *args, **kwargs):
    # print (kwargs)
    # region_id=kwargs['pk']
    # region_id = pk
    lakes = Lake.objects.filter (region=kwargs['pk'])
    # region_name = Region.objects.get(pk=kwargs).name
    region_name = 'test'
    kml = simplekml.Kml()
    for lake in lakes:
        kml.newpoint(
            name = lake.lake_info, 
            description = region_name,
            coords=[(lake.long,lake.lat)]
        )  # lon, lat optional height
        file_name = f'media/{region_name}.kml'
    kml.save(file_name)
    return render (request, 'catches/region_list.html', {})

def home (request):
    return render (request, 'catches/home.html', {})

class RegionListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_region'

    model = Region
    context_object_name = 'regions' 
    paginate_by = 6

class RegionDetailView (PermissionRequiredMixin, DetailView): 
    permission_required = 'catches.view_region'
    
    model = Region
    context_object_name = 'region'
    
    def get_context_data(self, **kwargs): 
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context ['lakes'] = Lake.objects.filter (region=self.kwargs['pk'])
        return context

class RegionCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_region'

    model = Region
    form_class = New_Regions_Form
    success_message = "New region saved"

class RegionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_region'

    model = Region
    form_class = New_Regions_Form
    success_message = "Region fixed"

class RegionDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_region'
    
    model = Region
    success_url = "/regions/"

 
class Fly_typeListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_fly_type'
    
    model = Fly_type
    context_object_name = 'fly_types' 
    paginate_by = 9

class Fly_typeDetailView (PermissionRequiredMixin, DetailView): 
    permission_required = 'catches.view_fly_type'
    
    model = Fly_type
    context_object_name = 'fly_type'
    
    def get_context_data(self, **kwargs): 
        context = super(Fly_typeDetailView, self).get_context_data(**kwargs)
        context ['flys'] = Fly.objects.filter (fly_type=self.kwargs['pk'])
        return context

class Fly_typeCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_fly_type'

    model = Fly_type
    fields = '__all__'    
    # form_class = New_Fly_type_Form
    # success_message = "New Fly type saved"

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The fly type was added'
        )
        return super().form_valid(form)


class Fly_typeUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_fly_type'

    model = Fly_type
    fields = '__all__'  
    # form_class = New_Fly_type_Form
    # success_message = "Fly type fixed"

class Fly_typeDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_fly_type'
    
    model = Fly_type
    success_url = "/fly_type/"


class FishListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_fish'
    
    model = Fish
    context_object_name = 'fishes' 
    paginate_by = 6
 
class FishDetailView (PermissionRequiredMixin, DetailView): 
    permission_required = 'catches.view_fish'
    
    model = Fish
    context_object_name = 'fish'
 
    def get_context_data(self, *args, **kwargs):
        context = super (FishDetailView, self).get_context_data (*args, **kwargs)
        data = Fish.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        return context

class FishCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_fish'

    model = Fish

    fields = '__all__' 
    # form_class = New_Fish_Form
    success_message = "New Fish saved"

class FishUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_fish'

    model = Fish
    fields = '__all__' 
    # form_class = New_Fish_Form
    success_message = "Fish fixed"

class FishDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_fish'
    
    model = Fish
    success_url = "/fish/"


class BugListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_bug'
    
    model = Bug
    context_object_name = 'bugs' 
    paginate_by = 9

class BugDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_bug'
    
    model = Bug
    context_object_name = 'bug'
    
    def get_context_data(self, **kwargs): 
        context = super(BugDetailView, self).get_context_data(**kwargs)
        context ['flys'] = Fly.objects.filter (bug=self.kwargs['pk'])
        data = Bug.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        return context

class BugCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_bug'

    model = Bug
    fields = '__all__' 
    # form_class = New_Bug_Form
    success_message = "New Bug saved"

class BugUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_bug'

    model = Bug
    fields = '__all__' 
    # form_class = New_Bug_Form
    success_message = "Bug fixed"

class BugDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_bug'
    
    model = Bug
    success_url = "/bug/"


class FlyListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_fly'
    
    model = Fly
    context_object_name = 'flys' 
    paginate_by = 6

class FlyDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_fly'
    
    model = Fly
    context_object_name = 'fly'
 
    def get_context_data(self, *args, **kwargs):
        context = super (FlyDetailView, self).get_context_data (*args, **kwargs)
        data = Fly.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos'] = Video.objects.filter (tags__name__contains=data)
        return context

class FlyCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_fly'

    model = Fly
    fields = '__all__'    
    
    def get_initial(self):
        if not self.kwargs:
            return
        if self.kwargs.get('field') == 'bug':
            model_to_use = Bug.objects.get(pk=self.kwargs['pk'])
        if self.kwargs.get('field') == 'fly_type':
            model_to_use = Fly_type.objects.get(pk=self.kwargs['pk'])
        return {self.kwargs.get('field'): model_to_use}

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The fly was added'
        )
        return super().form_valid (form)

class FlyUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_fly'

    model = Fly
    fields = '__all__'

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'fly fixed'
        )
        return super().form_valid (form)

class FlyDeleteView (PermissionRequiredMixin,  DeleteView):
    permission_required = 'catches.delete_fly'
    
    model = Fly
    success_url = "/flys/"


class LakeListView (UserAccessMixin, ListView):
    permission_required = 'catches.view_lake'
    model = Lake
    context_object_name = 'lakes' 
    paginate_by = 72


class LakeListView_regions (UserAccessMixin, TemplateView):
    permission_required = 'catches.view_lake'
    
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 30
    template_name = 'catches/templates/catches/lake_list.html'
 
    def get_context_data(self, *args, **kwargs):
        # print (self.kwargs)   
        context = super (LakeListView_regions, self).get_context_data (*args, **kwargs)
        context ['lakes'] = Lake.objects.filter (region=self.kwargs['pk'])
        return context


class LakeListView_fav (UserAccessMixin, TemplateView):
    permission_required = 'catches.view_lake'
    
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 15
    template_name = 'catches/templates/catches/lake_list.html'

    def get_context_data(self, *args, **kwargs):
        favourite = False
        if self.kwargs['favourite'] == 'True':
            favourite = True

        context = super (LakeListView_fav, self).get_context_data (*args, **kwargs)
        context ['lakes'] = Lake.objects.filter (favourite=favourite)
        context ['fav_count'] = Lake.objects.filter (favourite=favourite).count()
        return context


class LakeDetailView (UserAccessMixin, FormMixin, DetailView): 
    permission_required = 'catches.view_lake'
    
    model = Lake
    form_class = Plan_form
    # context_object_name = 'lake'

    def get_success_url(self, **kwargs):
        # print (f'self.weekpk = {self.weekpk}')
        # wpk = Week.objects.get(number=self.weekpk)
        # print (f'wpk = {wpk}')
        return reverse('plan', kwargs={'lpk': self.object.pk, 'wpk': self.weekpk})

    def get_context_data(self, **kwargs): 
        # context = super(LakeDetailView, self).get_context_data(**kwargs)
        stock_list = Stock.objects.filter (lake=self.kwargs['pk'])
        year_list = []
        for x in stock_list:
            if not x.date_stocked.year in year_list:
                year_list.append(x.date_stocked.year)
        subtotals = []
        total = 0
        for years in year_list:
            sub_t = 0
            for x in stock_list:
                if years == x.date_stocked.year:
                    sub_t += x.number
            subtotals.append({'year': years, 'subt': sub_t})
            total += sub_t
        subtotals.append({'year': 'total', 'subt': total})
        # print (subtotals)
        # lake_dist = Lake.objects.get(id=self.kwargs['pk'])
        # distance_to_lake = distance (lake_dist.lat, lake_dist.long)
        current_weather = weather_data (Lake.objects.get (id=self.kwargs['pk']))
        
        context = super().get_context_data(**kwargs)
        context ['lakes'] = Lake.objects.filter (id=self.kwargs['pk'])
        context ['stockings'] = stock_list
        context ['subts'] = subtotals 
        context ['logs'] = Log.objects.filter (lake=self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (lake=self.kwargs['pk'])
        data = Lake.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['pictures_list_bath'] = Picture.objects.filter (tags__name__contains=data) & Picture.objects.filter (tags__name__contains='bathymetric')
        context ['form'] = Plan_form()
        if current_weather != "":
            context ['current'] = current_weather  #<class 'dict'>
            context ['forecast'] = five_day_forcast (Lake.objects.get (id=self.kwargs['pk']))  #<class 'dict'>
        context ['distance'] = find_dist (Lake.objects.get (id=self.kwargs['pk']))  #<class 'dict'>
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        for key, value in request.POST.items():
            if key == "number":
                self.weekpk = value
        return self.form_valid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class LakeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_lake'
    
    model = Lake
    form_class = New_Lake_Form
    success_message = "New Lake saved"

class LakeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_lake'
    
    model = Lake
    form_class = New_Lake_Form
    success_message = "Lake fixed"

class LakeDeleteView (PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_lake'
    
    model = Lake
    success_url = "/lakes/"


class TempListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_temp'
    
    model = Temp
    context_object_name = 'temps' 
    paginate_by = 12

class TempDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_temp'
    
    model = Temp
    context_object_name = 'temp'
    
    def get_context_data(self, **kwargs): 
        context = super(TempDetailView, self).get_context_data(**kwargs)
        context ['chart_for_weeks'] = get_query_set(self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['pk']).order_by('temp')
        context ['temps'] = Temp.objects.filter (week=self.kwargs['pk']).order_by('id')
        context ['weeks'] = get_weeks (self.kwargs['pk'])
        context ['logs'] = Log.objects.filter (temp=self.kwargs['pk'])
        return context

class TempCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_temp'

    model = Temp
    form_class = New_Temp_Form
    success_message = "New Temp saved"

class TempUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_temp'

    model = Temp
    form_class = New_Temp_Form
    success_message = "Temp fixed"

class TempDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_temp'
    
    model = Temp
    success_url = "/temp/"


class HatchListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_hatch'
    
    model = Hatch
    context_object_name = 'hatchs' 
    paginate_by = 6

class HatchDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_hatch'
    model = Hatch
    context_object_name = 'hatch'

class HatchCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

class HatchCreateView_from_lake(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

    def get_initial(self):
        lake = Lake.objects.get(pk=self.kwargs['pk'])
        return {'lake': lake}

class HatchCreateView_from_bug(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

    def get_initial(self):
        bug = Bug.objects.get(pk=self.kwargs['pk'])
        return {'bug': bug}


class HatchUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "Hatch fixed"

class HatchDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_hatch'
    
    model = Hatch
    success_url = "/hatch/"


class WeekListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_week'
    model = Week
    context_object_name = 'weeks' 
    paginate_by = 20

class WeekDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_week'
    model = Week
    context_object_name = 'week'
    
    def get_context_data(self, **kwargs): 
        context = super(WeekDetailView, self).get_context_data(**kwargs)
        context ['chart_for_weeks'] = get_query_set (self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['pk']).order_by('temp')
        context ['temps'] = get_temps(self.kwargs['pk'])
        context ['logs'] = Log.objects.filter (week=self.kwargs['pk'])
        return context


class LogListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_log'
    model = Log
    context_object_name = 'logs' 
    paginate_by = 6

class LogListView_search (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_log'
    model = Log
    context_object_name = 'logs' # this is the name that we are passing to the template
    paginate_by = 9
    template_name = 'log_list.html'

    def get_queryset(self):
        index = 0
        query = self.request.GET.get("q")
        # print ('query is: ' + query)
        templist = Temp.objects.all()
        for t in templist:
            if query in t.search_keys:
                # print (t.name)
                index = t.id
                break
        if index == 0:
            object_list = Log.objects.all()
        else:
            object_list = Log.objects.filter(temp = index)
        return object_list

class LogDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_log'
    model = Log
    context_object_name = 'log'

class LogCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

class LogCreateView_from_lake(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
        lake = Lake.objects.get(pk=self.kwargs['pk'])
        return {'lake': lake}

class LogDuplicateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
        initial = super(LogDuplicateView, self).get_initial()
        log = Log.objects.get(pk=self.kwargs['pk'])
        initial['lake'] = log.lake
        initial['fish'] = log.fish
        initial['temp'] = log.temp
        initial['catch_date'] = log.catch_date
        initial['record_date'] = timezone.now
        initial['location'] = log.location
        initial['length'] = log.length
        initial['weight'] = log.weight
        initial['fly'] = log.fly
        initial['fly_size'] = log.fly_size
        initial['fly_colour'] = log.fly_colour
        initial['notes'] = log.notes
        initial['num_landed'] = log.num_landed
        initial['fish_swami'] = log.fish_swami
        initial['pk'] = None
        return initial

class LogCreateView_from_temp(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
     temp = Temp.objects.get(pk=self.kwargs['pk'])
     return {'temp': temp}

class LogUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_log'
    model = Log
    form_class = New_Log_Form
    success_message = "Log fixed"

class LogDeleteView (PermissionRequiredMixin,  DeleteView):
    permission_required = 'catches.delete_log'
    model = Log
    success_url = "/log/"

 
class StockListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_stock'
    model = Stock
    context_object_name = 'stocks' 
    paginate_by = 12

class StockDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_stock'
    model = Stock
    context_object_name = 'stock'

class StockCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_stock'
    model = Stock
    form_class = New_Stock_Form
    success_message = "New Stock saved"

class StockUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_stock'
    model = Stock
    form_class = New_Stock_Form
    success_message = "Stock fixed"

class StockDeleteView (PermissionRequiredMixin,  DeleteView): 
    permission_required = 'catches.delete_stock'
    model = Stock
    success_url = "/stock/"


class VideoListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_video'
    model = Video
    paginate_by = 12
    context_object_name = 'videos_list' 
 
class VideoDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_video'
    model = Video

class VideoCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_video'
    model = Video
    # form_class = Video_Form
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}
    
    def get_success_url(self):
        if not self.kwargs:
            return reverse('videos_list')
        if self.kwargs.get('field') == 'video':
            return reverse ('library_list')
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})
        

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The video was added'
        )
        return super().form_valid (form)

class VideoUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_video'
    model = Video
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')
    
    def get_success_url(self):
        if not self.kwargs:
            return reverse('videos_list')
        if self.kwargs.get('field') == 'video':
            return reverse ('library_list')
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Video fixed'
        )
        return super().form_valid (form)

class VideoDeleteView (PermissionRequiredMixin,  DeleteView):
    permission_required = 'catches.delete_video'
    model = Video
    success_url = reverse_lazy('videos_list')


class ArticleListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_article'
    model = Article
    paginate_by = 12
    context_object_name = 'articles_list' 
 
class ArticleDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_article'
    model = Article

class ArticleCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_article'
    model = Article
    # form_class = Article_Form
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}
    
    def get_success_url(self):
        if not self.kwargs:
            return reverse('articles_list')
        if self.kwargs.get('field') == 'article':
            return reverse ('library_list')
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The article was added'
        )
        return super().form_valid (form)

class ArticleUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_article'
    model = Article
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')
    
    def get_success_url(self):
        if not self.kwargs:
            return reverse('articles_list')
        if self.kwargs.get('field') == 'article':
            return reverse ('library_list')
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Article fixed'
        )
        return super().form_valid (form)

class ArticleDeleteView (PermissionRequiredMixin,  DeleteView):
    permission_required = 'catches.delete_article'
    model = Article
    success_url = reverse_lazy('articles_list')


class PictureListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_picture'
    model = Picture
    paginate_by = 2
    context_object_name = 'pictures_list'
 
class PictureDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_picture'
    model = Picture

class PictureCreateView(PermissionRequiredMixin,  CreateView):
    permission_required = 'catches.add_picture'
    model = Picture
    # form_class = Picture_Form
    fields = ('name', 'notes', 'tags', 'image', 'snippet')
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}
    
    def get_success_url(self):
        if not self.kwargs:
            return reverse('pictures_list')
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The picture was added'
        )
        return super().form_valid (form)

class PictureUpdateView(PermissionRequiredMixin,  UpdateView):
    permission_required = 'catches.change_picture'
    model = Picture
    fields = ('name', 'notes', 'tags', 'image', 'snippet')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Picture fixed'
        )
        return super().form_valid (form)
 
class PictureDeleteView (PermissionRequiredMixin,  DeleteView):
    permission_required = 'catches.delete_picture'
    model = Picture
    success_url = reverse_lazy('pictures_list')


def TagsListView(request):
    all_tags = Tag.objects.all().order_by('name')
    context = { 'tags_list': all_tags }
    return render (request, 'catches/tags_list.html', context)

def TagsDetailView(request, pk):
    tag = Tag.objects.filter(pk=pk)
    context = { 'tag': tag[0] }
    context ['videos_list'] = Video.objects.filter (tags__name__contains=tag[0])
    context ['articles_list'] = Article.objects.filter (tags__name__contains=tag[0])
    context ['pictures_list'] = Picture.objects.filter (tags__name__contains=tag[0])
    context ['flys'] = Fly.objects.filter (static_tag=tag[0].name)
    context ['lakes'] = Lake.objects.filter (static_tag=tag[0].name)
    context ['bugs'] = Bug.objects.filter (static_tag=tag[0].name)
    context ['fishes'] = Fish.objects.filter (static_tag=tag[0].name)
    return render (request, 'catches/tags_detail.html', context)

class Graph(TemplateView):
    template_name = 'catches/graph.html'
    context_object_name = 'graph'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        data = collect_tw_from_logs_and_hatches()

        df = pd.DataFrame.from_dict( data )
        df.columns = [ 'Week', 'week_id', 'Date', 'Temperature', 'temp_id', 'Temperature Name', 'log', 'type' ]
        
        df = df.sort_values(by='temp_id')
        # df = df.groupby(df.Date.dt.year)
        df.to_csv('graph_data.csv')

        fig = px.scatter(df, 
            x='Week',
            y='Temperature',
            trendline="rolling", 
            trendline_options=dict(window=5),
            height = 750,
            text='Date'
            )

        context = {'graph': fig.to_html()}
        return context

class ChartGraph(TemplateView):
    template_name = 'catches/chart_graph.html'
    context_object_name = 'graph'

    def get_context_data(self, **kwargs):
        context = super(ChartGraph, self).get_context_data(**kwargs)
        chart = Chart.objects.filter(bug=kwargs['pk'])

        data = []
        for row in chart:
            data.append ({'bug': row.bug.name, 'week': row.week.number, 'strength': row.strength})

        df = pd.DataFrame(data)
        table = df.pivot_table ('strength','week', 'bug')

        fig = px.area( table )

        context = {'graph': fig.to_html()}
        # context = {'bug': Bug.objects.filter(pk = kwargs['pk'])}

        return context    
        
def get_hl (id):
    temp_list = get_temps(id)
    # print (f'id is {id}   and temp_list is {temp_list}')
    low = 100
    high = 0
    for temp in temp_list:
        if temp['temp'] < low:
            low = temp['temp']
        if temp['temp'] > high:
            high = temp['temp']
    # print (f'low: {low} high: {high}')
    if low == 100:
        return {"low": '', "high": ''}
    else:
        return {"low": low, "high": high}

def fly_list(id):
    # id = 8
    logs = Log.objects.filter(week = id)
    fly_list = []
    for log in logs:
        if log.fly:
            fly_list.append(log.fly)
    fly_list = list(dict.fromkeys(fly_list))
    return fly_list  

    
class Plan(TemplateView):
    model = Lake
    template_name = 'catches/plan.html'
    context_object_name = 'lake'

    def get_context_data(self, **kwargs): 
        context = super(Plan, self).get_context_data(**kwargs)
        current_week = int(timezone.now().strftime("%W"))
        # check to see tht everyting we need is passed in and is correct.  
        # Then get the approperate data an dput it in the contect list
        context ['lake'] = Lake.objects.get (id=self.kwargs['lpk'])
        # print ('Lake worked')
        context ['week'] = Week.objects.get (id= self.kwargs['wpk'])
        # print ('Week worked')
        context ['temps'] = Temp.objects.filter (week=self.kwargs['wpk']).order_by('id')
        # print ('temps worked')
        context ['hl'] = get_hl (self.kwargs['wpk'])
        # print ('hl worked')
        # send the flys list to the context list
        context ['fly_list'] = fly_list (self.kwargs['wpk'])
        # print ('fly worked')
        # grab all the chart data
        chart_data = get_query_set (self.kwargs['wpk'])
        chart_list =[]
        for c in chart_data:
            if ( c['this'] == "abundent" or c['this'] == "lots" or c['trend'] == "rising" ):
                chart_list.append (c)
        # send all chart data that passed filter to context list
        context ['chart_for_weeks'] = chart_list
        # print ('chart_for_weeks worked')
        # send all hatch data for that week to contect list.
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['wpk'])
        # print ('hatches worked')
        array_list = get_array(
            week = self.kwargs['wpk'], 
            lake = self.kwargs['lpk'], 
            temperature = get_hl (self.kwargs['wpk'])['low']
        )
        context ['array'] = array_list
        # print ('array  worked')
        return context

INFO_LIST = [
    {'tag': 'how-to-fish', 'title': 'How To Fish', 'description': 'How-to information', 
     'image': '/media/pictures/Cardiff.jpeg'},
    {'tag': 'equipment', 'title': 'Equipment', 'description': 'Equipment specific information', 
     'image': '/media/pictures/fly_rods.jpeg'},
    {'tag': 'technique', 'title': 'Technique', 'description': 'Different Techniques', 
     'image': '/media/pictures/Cardiff_May_2022.jpeg'},
    {'tag': 'ice-out', 'title': 'Ice out', 'description': 'Fishing right after ice out', 
     'image': '/media/pictures/Cardiff_April_2022.jpeg'},
    {'tag': 'spring', 'title': 'Spring fishing', 'description': 'Fishing in the spring', 
     'image': '/media/pictures/Cardiff_May_2022_3.jpeg'},
    {'tag': 'fall', 'title': 'Fall fishing', 'description': 'Fall fishing', 
     'image': '/media/pictures/Cardiff_May_2022_2.jpeg'},
    {'tag': 'heat', 'title': 'Fishing in the heat', 'description': 'How to fish in the heat', 
     'image': '/media/pictures/Hay_lakes.jpeg'},
    {'tag': 'hatch', 'title': 'Hatch and Entimology', 'description': 'Hatch and Entimology', 
     'image': '/media/bug/dragon_nymph.jpeg'},
    {'tag': 'misc', 'title': 'Miscellaneous', 'description': 'Miscellaneous information', 
     'image': '/media/pictures/Cardiff.jpeg'},
]
    
class LibraryListView(TemplateView):
    model = Tag
    template_name = 'catches/library_list.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs): 
        context = super(LibraryListView, self).get_context_data(**kwargs)
        context ['info_list'] = INFO_LIST
        return context
    
class LibraryDetailView(TemplateView):
    model = Tag
    template_name = 'catches/library_detail.html'
    context_object_name = 'tag'  

    def get_context_data(self, **kwargs): 
        context = super(LibraryDetailView, self).get_context_data(**kwargs)
        tag_to_use = self.kwargs['tag']
        tag_info = list(filter(lambda tag: tag['tag'] == tag_to_use, INFO_LIST))
        tag_detail = tag_info[0].get('tag')
        context ['tag'] = tag_info[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains = tag_detail )
        context ['articles_list'] = Article.objects.filter (tags__name__contains = tag_detail )
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains = tag_detail )
        return context
    

def searchview (request):
    # paginate_by = 30
    template_name = 'catches/search_results.html'

    # request = self.request
    query = request.GET.get("q",'')
    # print (f'query = {query}')

    lake_results = Lake.objects.filter( 
        Q(name__icontains=query) | Q(other_name__icontains=query) | Q(district__icontains=query) | Q(static_tag__icontains=query)
    ) 
    region_results = Region.objects.filter( Q(name__icontains=query) )
    fish_results = Fish.objects.filter( Q(name__icontains=query) | Q(abbreviation__icontains=query) | Q(static_tag__icontains=query))
    bug_results = Bug.objects.filter( Q(name__icontains=query)  | Q(description__icontains=query) | Q(static_tag__icontains=query))
    fly_results = Fly.objects.filter( Q(name__icontains=query)   | Q(static_tag__icontains=query))
    video_results = Video.objects.filter( Q(name__icontains=query)  | Q(url__icontains=query) )
    picture_results = Picture.objects.filter( Q(name__icontains=query) )
    article_results = Article.objects.filter( Q(name__icontains=query) )

    context = {'lakes': lake_results, 'lakes_count': lake_results.count(),
               'regions': region_results, 'regions_count': region_results.count(),
               'fishes': fish_results, 'fishes_count': fish_results.count(),
               'bugs': bug_results, 'bugs_count': bug_results.count(),
               'flys': fly_results, 'flys_count': fly_results.count(),
               'videos': video_results, 'videos_count': video_results.count(),
               'pictures': picture_results, 'pictures_count': picture_results.count(),
               'articles': article_results, 'articles_count': article_results.count(),
               'query': query
               }

    return render( request, 'catches/search_results.html', context )
    # return context
