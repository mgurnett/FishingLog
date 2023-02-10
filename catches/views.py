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

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin   # this is how we limit not allowing non-logged in users from entering a lake
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from catches.forms import *

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
    return data

def get_query_set(pk): # get the data for the hatch trends for week detail view

    week_data = Week.objects.get(id=pk)
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
    # print (all_weeks)
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

class RegionListView (ListView):
    model = Region
    context_object_name = 'regions' 
    paginate_by = 6

class RegionDetailView (DetailView): 
    model = Region
    context_object_name = 'region'
    
    def get_context_data(self, **kwargs): 
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context ['lakes'] = Lake.objects.filter (region=self.kwargs['pk'])
        return context

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
    paginate_by = 9

class Fly_typeDetailView (DetailView): 
    model = Fly_type
    context_object_name = 'fly_type'
    
    def get_context_data(self, **kwargs): 
        context = super(Fly_typeDetailView, self).get_context_data(**kwargs)
        context ['flys'] = Fly.objects.filter (fly_type=self.kwargs['pk'])
        return context

class Fly_typeCreateView(LoginRequiredMixin, CreateView):
    model = Fly_type
    form_class = New_Fly_type_Form
    success_message = "New Fly type saved"

class Fly_typeUpdateView(LoginRequiredMixin, UpdateView):
    model = Fly_type
    form_class = New_Fly_type_Form
    success_message = "Fly type fixed"

class Fly_typeDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Fly_type
    success_url = "/fly_type/"


class FishListView (ListView):
    model = Fish
    context_object_name = 'fishes' 
    paginate_by = 6
 
class FishDetailView (DetailView): 
    model = Fish
    context_object_name = 'fish'
 
    def get_context_data(self, *args, **kwargs):
        context = super (FishDetailView, self).get_context_data (*args, **kwargs)
        data = Fish.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        return context

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
    paginate_by = 9

class BugDetailView (DetailView): 
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
 
    def get_context_data(self, *args, **kwargs):
        context = super (FlyDetailView, self).get_context_data (*args, **kwargs)
        data = Fly.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos'] = Video.objects.filter (tags__name__contains=data)
        return context

class FlyCreateView(LoginRequiredMixin, CreateView):
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

class FlyUpdateView(LoginRequiredMixin, UpdateView):
    model = Fly
    fields = '__all__'

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'fly fixed'
        )
        return super().form_valid (form)

class FlyDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Fly
    success_url = "/flys/"


class LakeListView (ListView):
    model = Lake
    context_object_name = 'lakes' 
    paginate_by = 72

class LakeListView_search (ListView):
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 30
    template_name = 'lake_list.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Lake.objects.filter(
            Q(name__icontains=query) | Q(other_name__icontains=query) | Q(district__icontains=query)
        )
        return object_list

class LakeListView_regions (TemplateView):
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 30
    template_name = 'catches/templates/catches/lake_list.html'
 
    def get_context_data(self, *args, **kwargs):
        print (self.kwargs)
        context = super (LakeListView_regions, self).get_context_data (*args, **kwargs)
        context ['lakes'] = Lake.objects.filter (region=self.kwargs['pk'])
        return context

class LakeListView_fav (TemplateView):
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

# class Plan2_Form(forms.Form):
#     number = forms.CharField()

class LakeDetailView (FormMixin, DetailView): 
    model = Lake
    form_class = Plan_form
    # context_object_name = 'lake'

    def get_success_url(self, **kwargs):
        wpk = Week.objects.get(number=self.weekpk)
        # print (f'wpk = {wpk}')
        return reverse('plan', kwargs={'lpk': self.object.pk, 'wpk': wpk})

    def get_context_data(self, **kwargs): 
        # context = super(LakeDetailView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context ['lakes'] = Lake.objects.filter (id=self.kwargs['pk'])
        context ['stockings'] = Stock.objects.filter (lake=self.kwargs['pk'])
        context ['logs'] = Log.objects.filter (lake=self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (lake=self.kwargs['pk'])
        data = Lake.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['pictures_list_bath'] = Picture.objects.filter (tags__name__contains=data) & Picture.objects.filter (tags__name__contains='bathymetric')
        context ['form'] = Plan_form()
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
    success_url = "/lakes/"


class TempListView (ListView):
    model = Temp
    context_object_name = 'temps' 
    paginate_by = 12

class TempDetailView (DetailView): 
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


class HatchListView (ListView):
    model = Hatch
    context_object_name = 'hatchs' 
    paginate_by = 6

class HatchDetailView (DetailView): 
    model = Hatch
    context_object_name = 'hatch'

class HatchCreateView(LoginRequiredMixin, CreateView):
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

class HatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "Hatch fixed"

class HatchDeleteView (LoginRequiredMixin, DeleteView):    #https://youtu.be/-s7e_Fy6NRU?t=2344
    model = Hatch
    success_url = "/hatch/"


class WeekListView (ListView):
    model = Week
    context_object_name = 'weeks' 
    paginate_by = 20

class WeekDetailView (DetailView): 
    model = Week
    context_object_name = 'week'
    
    def get_context_data(self, **kwargs): 
        context = super(WeekDetailView, self).get_context_data(**kwargs)
        context ['chart_for_weeks'] = get_query_set (self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['pk']).order_by('temp')
        context ['temps'] = get_temps(self.kwargs['pk'])
        context ['logs'] = Log.objects.filter (week=self.kwargs['pk'])
        return context


class LogListView (ListView):
    model = Log
    context_object_name = 'logs' 
    paginate_by = 6

class LogListView_search (ListView):
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

class LogDetailView (DetailView): 
    model = Log
    context_object_name = 'log'

class LogCreateView(LoginRequiredMixin, CreateView):
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

class LogCreateView_from_lake(LoginRequiredMixin, CreateView):
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
        lake = Lake.objects.get(pk=self.kwargs['pk'])
        return {'lake': lake}

class LogDuplicateView(LoginRequiredMixin, CreateView):
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

class LogCreateView_from_temp(LoginRequiredMixin, CreateView):
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
     temp = Temp.objects.get(pk=self.kwargs['pk'])
     return {'temp': temp}

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
    paginate_by = 12

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


class VideoListView(ListView):
    model = Video
    paginate_by = 12
    context_object_name = 'videos_list' 
 
class VideoDetailView(DetailView):
    model = Video

class VideoCreateView(LoginRequiredMixin, CreateView):
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
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The video was added'
        )
        return super().form_valid (form)

class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Video fixed'
        )
        return super().form_valid (form)

class VideoDeleteView (LoginRequiredMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('videos_list')


class ArticleListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'articles_list' 
 
class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(LoginRequiredMixin, CreateView):
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
        model_to_use = f"{self.kwargs.get('field')}_detail"
        return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The article was added'
        )
        return super().form_valid (form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Article fixed'
        )
        return super().form_valid (form)

class ArticleDeleteView (LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles_list')


class PictureListView(ListView):
    model = Picture
    paginate_by = 2
    context_object_name = 'pictures_list'
 
class PictureDetailView(DetailView):
    model = Picture

class PictureCreateView(LoginRequiredMixin, CreateView):
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

class PictureUpdateView(LoginRequiredMixin, UpdateView):
    model = Picture
    fields = ('name', 'notes', 'tags', 'image', 'snippet')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Picture fixed'
        )
        return super().form_valid (form)
 
class PictureDeleteView (LoginRequiredMixin, DeleteView):
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
        
        df = df.sort_values(by='Week')

        fig = px.scatter(df, 
            x='Week',
            y='Temperature',
            trendline="rolling", 
            trendline_options=dict(window=5),
            height = 750,
            text='Date'
            )

        context= {'graph': fig.to_html()}
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

def plan_setup (request):
    return render (request, 'catches/plan_setup.html', {})

    
class Plan(TemplateView):
    model = Lake
    template_name = 'catches/plan.html'
    context_object_name = 'lake'

    def get_context_data(self, **kwargs): 
        context = super(Plan, self).get_context_data(**kwargs)
        current_week = int(timezone.now().strftime("%W"))

        context ['lake'] = Lake.objects.get (id=self.kwargs['lpk'])
        context ['week'] = Week.objects.get (id= self.kwargs['wpk'])
        context ['temps'] = Temp.objects.filter (week=self.kwargs['wpk']).order_by('id')
        context ['hl'] = get_hl (self.kwargs['wpk'])
        context ['fly_list'] = fly_list (self.kwargs['wpk'])
        chart_data = get_query_set (self.kwargs['wpk'])
        chart_list =[]
        for c in chart_data:
            if ( c['this'] == "abundent" or c['this'] == "lots" or c['trend'] == "rising" ):
                chart_list.append (c)
        context ['chart_for_weeks'] = chart_list
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['wpk'])
        return context