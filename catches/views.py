from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy

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
    context_object_name = 'fishes'
 
    def get_context_data(self, *args, **kwargs):
        context = super (FishDetailView, self).get_context_data (*args, **kwargs)
        data = Fish.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos'] = Video.objects.filter (tags__name__contains=data)
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
        context ['videos'] = Video.objects.filter (tags__name__contains=data)
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

# class FlyCreateView(LoginRequiredMixin, CreateView):
#     model = Fly
#     form_class = New_Fly_Form
#     success_message = "New Fly saved"

# class FlyUpdateView(LoginRequiredMixin, UpdateView):
#     model = Fly
#     form_class = New_Fly_Form
#     success_message = "Fly fixed"

class FlyCreateView(LoginRequiredMixin, CreateView):
    model = Fly
    fields = '__all__'

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
    paginate_by = 46

class LakeListView_search (ListView):
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 30
    template_name = 'lake_list.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Lake.objects.filter(
            Q(name__icontains=query) | Q(district__icontains=query)
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
        context ['fav_count'] = Lake.objects.filter (favourite=favourite).count()
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

class LakeDetailView (DetailView): 
    model = Lake
    context_object_name = 'lake'
    
    def get_context_data(self, **kwargs): 
        context = super(LakeDetailView, self).get_context_data(**kwargs)
        context ['lakes'] = Lake.objects.filter (id=self.kwargs['pk'])
        context ['stockings'] = Stock.objects.filter (lake=self.kwargs['pk'])
        context ['logs'] = Log.objects.filter (lake=self.kwargs['pk'])
        data = Lake.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos'] = Video.objects.filter (tags__name__contains=data)
        context ['articles'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures'] = Picture.objects.filter (tags__name__contains=data)
        return context

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
    paginate_by = 10

class TempDetailView (DetailView): 
    model = Temp
    context_object_name = 'temp'
    
    def get_context_data(self, **kwargs): 
        context = super(TempDetailView, self).get_context_data(**kwargs)
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

class LogListView_search (ListView):
    model = Log
    context_object_name = 'logs' # this is the name that we are passing to the template
    paginate_by = 9
    template_name = 'log_list.html'

    def get_queryset(self):
        index = 0
        query = self.request.GET.get("q")
        print ('query is: ' + query)
        templist = Temp.objects.all()
        for t in templist:
            if query in t.search_keys:
                print (t.name)
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
 
class VideoDetailView(DetailView):
    model = Video

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    # form_class = Video_Form
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')

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
 
class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    # form_class = Article_Form
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')

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
    paginate_by = 12
 
class PictureDetailView(DetailView):
    model = Picture

class PictureCreateView(LoginRequiredMixin, CreateView):
    model = Picture
    # form_class = Picture_Form
    fields = ('name', 'notes', 'tags', 'image', 'snippet')

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