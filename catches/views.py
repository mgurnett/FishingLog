from django.shortcuts import render, redirect
from .models import *
from blog.models import *
from users.models import Profile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.http import HttpResponse, FileResponse
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy  #lets you call urls by name 
from django.core.management import BaseCommand
from django.template.defaultfilters import slugify
from taggit.models import Tag
import pandas as pd
import plotly.express as px

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
from .Open_Weather import *
from .distance import *
from .queries import *

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

class Home (TemplateView): 
    template_name = 'catches/home.html'
    model = Announcment

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        announces = Announcment.objects.all()
        announce_list = []
        trip_str = ""
        for an in announces:
            if an.lake_id != 0:
                lake = Lake.objects.get(pk=an.lake_id)
                trip_str = f'Our next planned trip is: <b>{lake.name}</b> {an.notes}'
            else:
                announce_list.append (an.notes)
        context ['announcments'] = announce_list
        context ['trip'] = trip_str
        context ['lake_link'] = trip_str
        return context

class RegionListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_region'
    model = Region
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        profile_ob = convert_user_to_profile (self.request.user)  # I have to convert user id into profile.   They are not the same.
        context = super (RegionListView, self).get_context_data (*args, **kwargs)
        context ['regions'] = Region.objects.filter (profile = profile_ob)
        # context ['regions'] = Region.objects.all()
        return context

class RegionDetailView(PermissionRequiredMixin, FormMixin, DetailView):
    permission_required = 'catches.view_region'
    model = Region
    form_class = Lake_to_Region_form

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('region_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lakes'] = get_lakes_for_user_by_region(self.kwargs['pk'], self.request.user.id)
        context['form'] = self.get_form()  # Use get_form() for consistency
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form() 

        if form.is_valid():
            # Set the lake instance as an attribute on the view (more explicit)
            cleaned_lake = form.cleaned_data['lake']
            self.lake = Lake.objects.get(pk=cleaned_lake.id)
            return self.form_valid(form, request)

    # Handle form validation and lake association
    def form_valid(self, form, request):
        lake_id = form.cleaned_data['lake']  # Access the lake's ID from cleaned data
        self.lake = Lake.objects.get(pk=lake_id.id)  # Retrieve the lake instance
        self.object.lakes.add(self.lake)  # Add the lake to the region
        mess = f'{self.lake.name} added to region'
        messages.info(request, mess)
        return super().form_valid(form)

class RegionCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_region'
    model = Region
    form_class = New_Regions_Form
    success_message = "New region saved"

    def form_valid(self, form):
        profile = Profile.objects.get (user = self.request.user)
        form.instance.profile = profile
        return super().form_valid(form)

class RegionUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_region'
    model = Region
    form_class = New_Regions_Form
    success_message = "Region fixed"

    def form_valid(self, form):
        profile = Profile.objects.get (user = self.request.user)
        form.instance.profile = profile
        return super().form_valid(form)

class RegionDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_region'
    model = Region
    success_url = "/regions/"
    success_message = "Region deleted"

def remove_lake_from_region(request, pk, lake_pk):
    region = Region.objects.get(pk=pk)
    lake = Lake.objects.get(pk=lake_pk)

    if request.method == 'POST':
        region.lakes.remove(lake)
        mess_text = f'<b>{lake.name}</b> removed from {region.name}'
        messages.add_message(request, messages.ERROR, mess_text)
        # Success message or logic (optional)
        return redirect('region_detail', pk=pk)

    # Render confirmation template or handle GET requests (optional)
    return render(request, 'template/confirmation.html', {'region': region, 'lake': lake})

 
class FavoriteListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_favorite'
    model = Favorite
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        favs = Favorite.objects.filter (user = self.request.user)
        count = favs.count()
        context = super (FavoriteListView, self).get_context_data (*args, **kwargs)
        context ['favorites'] = favs
        context ['count'] = count
        return context

def remove_lake_from_favorites(request, pk):
    favorite = Favorite.objects.get(pk=pk)
    lake_pk = favorite.lake.id
    if request.method == 'POST':
        favorite.delete()
        if 'lake_detail' in request.POST:
            mess_text = f'<b>{favorite.lake.name}</b> removed from your favorites'
            messages.add_message(request, messages.ERROR, mess_text)
            return redirect('lake_detail', lake_pk)
        # Success message or logic (optional)
    return redirect('favorite_list')
    
def add_lake_to_favorites(request, lake_pk, user_pk):
    lake = Lake.objects.get(pk=lake_pk)
    user = User.objects.get(pk=user_pk)
    favorite = Favorite (lake=lake, user=user)
    if request.method == 'POST':
        favorite.save()
        if 'lake_detail' in request.POST:
            mess_text = f'{lake.name} added to your favorites'
            messages.add_message(request, messages.ERROR, mess_text)
            return redirect('lake_detail', lake_pk)
        # Success message or logic (optional)
    return redirect('favorite_list')

 
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

class Fly_typeCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_fly_type'
    model = Fly_type
    fields = '__all__'
    success_message = "New Fly type saved"
    success_url = reverse_lazy ('fly_type_list')

class Fly_typeUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_fly_type'
    model = Fly_type
    fields = '__all__'  
    success_message = "Fly type fixed"
    success_url = reverse_lazy ('fly_type_list')

class Fly_typeDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_fly_type'
    
    model = Fly_type
    success_url = "/fly_type/"
    success_message = "Fly type deleted"


class FishListView (PermissionRequiredMixin, ListView):
    permission_required = 'catches.view_fish'
    
    model = Fish
    context_object_name = 'fishes' 
    paginate_by = 6
    
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return super(FishListView, self).handle_no_permission()
 
class FishDetailView (PermissionRequiredMixin, DetailView): 
    permission_required = 'catches.view_fish'
    model = Fish
    context_object_name = 'fish'
 
    def get_context_data(self, *args, **kwargs):

        stock_list = Stock.objects.filter (fish=self.kwargs['pk'])
        subtotals = stock_with_subtotals (stock_list)

        if self.request.user.is_authenticated:
            logs_list = log_filter_for_private (Log.objects.filter (fish=self.kwargs['pk']), self.request.user)
        else:
            logs_list = log_filter_for_private (Log.objects.filter (fish=self.kwargs['pk']), None)

        context = super (FishDetailView, self).get_context_data (*args, **kwargs)
        data = Fish.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['posts'] = Post.objects.filter (tags__name__contains = data)
        context ['stockings'] = stock_list
        context ['subts'] = subtotals 
        context ['logs'] = logs_list
        context ['model'] = "fish"
        return context

class FishCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_fish'
    model = Fish
    fields = '__all__' 
    # form_class = New_Fish_Form
    success_message = "New Fish saved"

class FishUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_fish'

    model = Fish
    fields = '__all__' 
    # form_class = New_Fish_Form
    success_message = "Fish fixed"

class FishDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_fish'
    
    model = Fish
    success_url = "/fish/"
    success_message = "Fish deleted"


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
        context ['hatches'] = Hatch.objects.filter (bug=self.kwargs['pk'])
        data = Bug.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['posts'] = Post.objects.filter (tags__name__contains = data)
        return context

class BugCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_bug'
    model = Bug
    form_class = New_Bug_Form
    success_url = reverse_lazy ('bug_list')
    success_message = "New Bug saved" 

    def form_valid(self, form):
        if not form.instance.static_tag:
            form.instance.static_tag = slugify(form.instance.name)
        return super().form_valid(form)

class BugUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_bug'
    model = Bug
    form_class = New_Bug_Form
    success_url = reverse_lazy ('bug_list')
    success_message = "Bug fixed"

    def form_valid(self, form):
        if not form.instance.static_tag:
            form.instance.static_tag = slugify(form.instance.name)
        return super().form_valid(form)

class BugDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_bug'
    model = Bug
    success_url = reverse_lazy ('bug_list')
    success_message = "Bug was deleted"


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
        if self.request.user.is_authenticated:
            logs_list = log_filter_for_private (Log.objects.filter (fly=self.kwargs['pk']), self.request.user)
        else:
            logs_list = log_filter_for_private (Log.objects.filter (fly=self.kwargs['pk']), None)

        context = super (FlyDetailView, self).get_context_data (*args, **kwargs)
        data = Fly.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['posts'] = Post.objects.filter (tags__name__contains = data)
        context ['logs'] = logs_list
        return context

class FlyCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
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

class FlyUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
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

class FlyDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_fly'
    model = Fly
    success_url = "/flys/"
    success_message = "Fly was deleted"


class LakeListView (ListView):
    # permission_required = 'catches.view_lake'
    model = Lake
    context_object_name = 'lakes' 

    def get_context_data(self, *args, **kwargs):

        dists_list = list(DISTRICTS)
        dists = []
        lake_num = 0
        for d in dists_list:
            dist_count = Lake.objects.filter ( district = d[0] ).count()
            di = (d[0], d[1], dist_count )
            dists.append(di)
            lake_num = lake_num + dist_count
        # print (f"Total lakes is: {lake_num}")

        if self.request.user.is_authenticated:
            fav_objs = Favorite.objects.filter (user=self.request.user)
            profile_ob = convert_user_to_profile (self.request.user)
            region_objs = Region.objects.filter (profile_id = profile_ob)
            # for fav in fav_objs:
            #     print (f'{fav.lake.lake_full_name = }')
        else:
            fav_objs = None
            region_objs = None
            # print ('Not autorized')


        context = super (LakeListView, self).get_context_data (*args, **kwargs)
        context ['favs'] = fav_objs  # a list of all lake that are this user's favorites.
        context ['regions'] = region_objs
        context ['districts'] = dists
        return context

class LakeListView_districts (SuccessMessageMixin, UserAccessMixin, TemplateView):
    permission_required = 'catches.view_lake'
    model = Lake
    context_object_name = 'lakes' # this is the name that we are passing to the template
    paginate_by = 30
    template_name = 'catches/lake_list_dist.html'
 
    def get_context_data(self, *args, **kwargs):
        dist = DISTRICTS[self.kwargs['pk']]  
        context = super (LakeListView_districts, self).get_context_data (*args, **kwargs)
        context ['lakes'] = Lake.objects.filter (district = dist[0])
        context ['district'] = dist[1]
        context ['id'] = dist[0]
        # context ['lake_count'] = Lake.objects.filter (district = dist[0]).count()
        return context
 
class LakeDetailView (FormMixin, DetailView):  
    # permission_required = 'catches.view_lake'
    model = Lake
    form_class = Plan_form
    # context_object_name = 'lake'

    def get_success_url(self, **kwargs):  #this is here due to plan form.
        # print (f'self.weekpk = {self.weekpk}')
        # wpk = Week.objects.get(number=self.weekpk)
        # print (f'wpk = {wpk}')
        return reverse('plan', kwargs={'lpk': self.object.pk, 'wpk': self.weekpk})

    def get_context_data(self, **kwargs): 
        # context = super(LakeDetailView, self).get_context_data(**kwargs)
        stock_list = Stock.objects.filter (lake=self.kwargs['pk'])
        subtotals = stock_with_subtotals (stock_list)

        week_now = int(timezone.now().strftime("%W"))
        
        if self.request.user.is_authenticated:
            distance_to_lake = find_dist (Lake.objects.get (id=self.kwargs['pk']), self.request.user)  #<class 'dict'>
            logs_list = log_filter_for_private (Log.objects.filter (lake=self.kwargs['pk']), self.request.user)    
            favorite_id = favorite_filter_for_lake (self.kwargs['pk'], self.request.user) 
        else:
            distance_to_lake = ""
            logs_list = log_filter_for_private (Log.objects.filter (lake=self.kwargs['pk']), None)

        if favorite_id:
            favorite_info = Favorite.objects.get(pk=favorite_id)
        else:
            favorite_info = None

        # current_weather = weather_data (Lake.objects.get (id=self.kwargs['pk']))

        data = Lake.objects.filter (id=self.kwargs['pk']).values_list('static_tag', flat=True)[0]

        context = super().get_context_data(**kwargs)
        context ['stockings'] = stock_list
        context ['subts'] = subtotals 
        context ['logs'] = logs_list 
        context ['hatches'] = Hatch.objects.filter (lake=self.kwargs['pk'])
        context ['fav'] = favorite_info
        context ['videos_list'] = Video.objects.filter (tags__name__contains=data)
        context ['articles_list'] = Article.objects.filter (tags__name__contains=data)
        context ['pictures_list'] = Picture.objects.filter (tags__name__contains=data)
        context ['pictures_list_bath'] = Picture.objects.filter (tags__name__contains=data) & Picture.objects.filter (tags__name__contains='bathymetric')
        context ['form'] = Plan_form()
        context ['ave_data'] = get_average_temp_for_week (week_now)
        # if current_weather != "":
        #     context ['current'] = current_weather  #<class 'dict'>
        #     context ['forecast'] = five_day_forcast (Lake.objects.get (id=self.kwargs['pk']))  #<class 'dict'>
        context ['distance'] = distance_to_lake
        context ['posts'] = Post.objects.filter (tags__name__contains = data)
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

class LakeCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_lake'
    model = Lake
    form_class = New_Lake_Form
    success_url = "/lakes/"
    success_message = "Lake was created successfully"

    def form_valid(self, form):
        if not form.instance.static_tag:
            form.instance.static_tag = slugify(form.instance.name)
        return super().form_valid(form)

class LakeUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_lake'
    model = Lake
    form_class = New_Lake_Form
    success_url = "/lakes/"
    success_message = "Lake was edited successfully"

    def form_valid(self, form):
        if not form.instance.static_tag:
            form.instance.static_tag = slugify(form.instance.name)
        return super().form_valid(form)

class LakeDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_lake'
    model = Lake
    success_url = "/lakes/"
    success_message = "Lake was deleted"


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
        context ['logs'] = log_filter_for_private (Log.objects.filter (temp=self.kwargs['pk']), self.request.user)
        return context

class TempCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_temp'
    model = Temp
    form_class = New_Temp_Form
    success_message = "New Temp saved"
    success_url = "/temps/"

class TempUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_temp'
    model = Temp
    form_class = New_Temp_Form
    success_message = "Note changed"
    reverse_lazy('temp_list')

class TempDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_temp'
    model = Temp
    success_url = "/temp/"
    success_message = "Temperature was deleted"


class HatchListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_hatch'
    model = Hatch
    context_object_name = 'hatchs' 
    paginate_by = 6

class HatchDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_hatch'
    model = Hatch
    context_object_name = 'hatch'

class HatchCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

class HatchCreateView_from_lake(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

    def get_initial(self):
        lake = Lake.objects.get(pk=self.kwargs['pk'])
        return {'lake': lake}

class HatchCreateView_from_bug(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "New Hatch saved"

    def get_initial(self):
        bug = Bug.objects.get(pk=self.kwargs['pk'])
        return {'bug': bug}

class HatchUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_hatch'
    model = Hatch
    form_class = New_Hatch_Form
    success_message = "Hatch fixed"

class HatchDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_hatch'
    model = Hatch
    success_url = "/hatch/"
    success_message = "Hatch was deleted"


class WeekListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_week'
    model = Week
    context_object_name = 'weeks' 
    paginate_by = 16 

class WeekDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_week'
    model = Week
    context_object_name = 'week'
    
    def get_context_data(self, **kwargs): 
        context = super(WeekDetailView, self).get_context_data(**kwargs)
        context ['chart_for_weeks'] = get_query_set (self.kwargs['pk'])
        context ['hatches'] = Hatch.objects.filter (week=self.kwargs['pk']).order_by('temp')
        context ['temps'] = get_temps(self.kwargs['pk'])
        context ['logs'] = log_filter_for_private (Log.objects.filter (week=self.kwargs['pk']), self.request.user)
        context ['model'] = "weeks"
        return context

 
class LogListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_log'
    model = Log
    context_object_name = 'logs' 
    paginate_by = 6

    def get_queryset(self):
        log_list = log_filter_for_private (Log.objects.all(), self.request.user)
        return log_list

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
            object_list_all = Log.objects.all()
        else:
            object_list_all = Log.objects.filter(temp = index)
        object_list = log_filter_for_private (object_list_all, self.request.user)
        return object_list

class LogDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_log'
    model = Log
    context_object_name = 'log'

class LogCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def form_valid(self, form):
        form.instance.angler = self.request.user  # Assign logged-in user
        return super().form_valid(form)

class LogCreateView_from_lake(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
        lake = Lake.objects.get(pk=self.kwargs['pk'])
        return {'lake': lake}

    def form_valid(self, form):
        form.instance.angler = self.request.user  # Assign logged-in user
        return super().form_valid(form)

class LogCreateView_from_temp(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_log'
    model = Log
    form_class = New_Log_Form
    success_message = "New Log saved"

    def get_initial(self):
     temp = Temp.objects.get(pk=self.kwargs['pk'])
     return {'temp': temp}

    def form_valid(self, form):
        form.instance.angler = self.request.user  # Assign logged-in user
        return super().form_valid(form)
    
class LogDuplicateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
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
        initial['private'] = log.private
        initial['pk'] = None
        return initial

    def form_valid(self, form):
        form.instance.angler = self.request.user  # Assign logged-in user
        return super().form_valid(form)

class LogUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_log'
    model = Log
    form_class = New_Log_Form
    success_message = "Log fixed"

class LogDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_log'
    model = Log
    success_url = "/log/"
    success_message = "Log was deleted"

 
class StockListView (PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_stock'
    model = Stock
    context_object_name = 'stocks' 
    paginate_by = 12

class StockDetailView (PermissionRequiredMixin,  DetailView): 
    permission_required = 'catches.view_stock'
    model = Stock
    context_object_name = 'stock'

class StockCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_stock'
    model = Stock
    form_class = New_Stock_Form
    success_message = "New Stock saved"

class StockUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_stock'
    model = Stock
    form_class = New_Stock_Form
    success_message = "Stock fixed"

class StockDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'catches.delete_stock'
    model = Stock
    success_url = "/stock/"
    success_message = "Stock record was deleted"


class VideoListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_video'
    model = Video
    paginate_by = 8
    context_object_name = 'videos_list' 
 
class VideoDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_video'
    model = Video

class VideoCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_video'
    model = Video
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')
    success_message = 'The video was added'
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}

class VideoUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_video'
    model = Video
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet')
    success_message = "Video fixed"
    
    # def get_success_url(self):
    #     if not self.kwargs:
    #         return reverse('videos_list')
    #     if self.kwargs.get('field') == 'video':
    #         return reverse ('library_list')
    #     model_to_use = f"{self.kwargs.get('field')}_detail"
    #     return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})
    
    def get_success_url(self):
        # return reverse('videos_list')
        return reverse('video_detail', kwargs={'pk': self.kwargs.get('pk')})

class VideoDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_video'
    model = Video
    success_url = reverse_lazy('videos_list')
    success_message = "Video was deleted"


class ArticleListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_article'
    model = Article
    paginate_by = 8
    context_object_name = 'articles_list' 
 
class ArticleDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_article'
    model = Article

class ArticleCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_article'
    model = Article
    # form_class = Article_Form
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}
    
    # def get_success_url(self):
    #     if not self.kwargs:
    #         return reverse('articles_list')
    #     if self.kwargs.get('field') == 'article':
    #         return reverse ('library_list')
    #     model_to_use = f"{self.kwargs.get('field')}_detail"
    #     print (model_to_use)
    #     return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})
    
    def get_success_url(self):
        return reverse ('library_list')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The article was added'
        )
        return super().form_valid (form)

class ArticleUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_article'
    model = Article
    fields = ('name', 'notes', 'author', 'tags', 'url', 'snippet', 'file')
    
    def get_success_url(self, **kwargs):
        # print (f"kwarg = {self.kwargs }")
        # if not self.kwargs:
        #     return reverse('articles_list')
        # if self.kwargs.get('field') == 'article':
        #     return reverse ('library_list')
        # model_to_use = f"{self.kwargs.get('field')}_detail"
        # print (f'{model_to_use = }')
        return reverse('article_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Article changed'
        )
        return super().form_valid (form)

class ArticleDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_article'
    model = Article
    success_url = reverse_lazy('articles_list')
    success_message = "Article was deleted"


class PictureListView(PermissionRequiredMixin,  ListView):
    permission_required = 'catches.view_picture'
    model = Picture
    paginate_by = 2
    context_object_name = 'pictures_list'
 
class PictureDetailView(PermissionRequiredMixin,  DetailView):
    permission_required = 'catches.view_picture'
    model = Picture

class PictureCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catches.add_picture'
    model = Picture
    # form_class = Picture_Form
    fields = ('name', 'notes', 'tags', 'image', 'snippet')
    
    def get_initial(self):
        if not self.kwargs:
            return
        tag = self.kwargs['tag']
        return {('tags'): tag}
    
    # def get_success_url(self):
    #     if not self.kwargs:
    #         return reverse('pictures_list')
    #     model_to_use = f"{self.kwargs.get('field')}_detail"
    #     return reverse(model_to_use, kwargs={'pk': self.kwargs.get('pk')})
    
    def get_success_url(self):
        return reverse('pictures_list')

    def form_valid (self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The picture was added'
        )
        return super().form_valid (form)

class PictureUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catches.change_picture'
    model = Picture
    fields = ('name', 'notes', 'tags', 'image', 'snippet')
    success_message = "Picture fixed"
 
class PictureDeleteView (SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catches.delete_picture'
    model = Picture
    success_url = reverse_lazy('pictures_list')
    success_message = "Picture was deleted"


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
    context ['posts'] = Post.objects.filter (tags__name__contains=tag[0].name)
    return render (request, 'catches/tags_detail.html', context)


class Graph (TemplateView):   # this is for all temps at all lakes
    template_name = 'catches/graph.html'
    context_object_name = 'graph'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        data = collect_tw_from_logs_and_hatches()

        df = pd.DataFrame.from_dict( data )
        df.columns = [ 'Week', 'week_id', 'Date', 'Temperature', 'temp_id', 'Temperature Name', 'log', 'type', 'year' ]
        # df['date'] = pd.to_datetime(df['date'])
        # df = df.set_index('date') 
        
        df = df.sort_values(by='temp_id')
        # df = df.groupby(pd.Grouper(key='Date', axis=0, freq='YS', sort=True)).sum()  
        # df = df.groupby(df.Date.dt.year)
        # df.to_csv('graph_data.csv')

        # fig = px.scatter(df, 
        #     x='Week',
        #     y='Temperature',
        #     trendline="rolling",  
        #     trendline_options=dict(window=10),
        #     height = 750,
        #     text='Date',
        #     color="year",
        #     )            
        fig = px.scatter(
            df, 
            x="Week", 
            y="Temperature", 
            color = "year",
            trendline_scope="overall",
            trendline="lowess",
            trendline_options=dict(frac=0.1),
            height = 750,
            hover_name='Date'
        )
        fig.update_traces(marker=dict(size=20))

        context = {'graph': fig.to_html()}
        return context

class Graph_lake (TemplateView):   # this is for all temps at one lakes
    template_name = 'catches/graph.html'
    context_object_name = 'graph'

    def get_context_data(self, **kwargs):
        context = super(Graph_lake, self).get_context_data(**kwargs)

        lake = Lake.objects.get(pk=self.kwargs['pk'])

        data = collect_tw_from_logs_and_hatches(lake=lake)
        if data:

            df = pd.DataFrame.from_dict( data )
            df.columns = [ 'Week', 'week_id', 'Date', 'Temperature', 'temp_id', 'Temperature Name', 'log', 'type', 'year' ]
            
            df = df.sort_values(by='temp_id')

            fig = px.scatter(
                df, 
                x="Week", 
                y="Temperature", 
                color = "year",
                trendline_scope="overall",
                trendline="lowess",
                trendline_options=dict(frac=0.1),
                height = 750,
                hover_name='Date'
            )
            fig.update_traces(marker=dict(size=20))

            context = {'graph': fig.to_html()}
            context ['lake'] = lake
            return context
        else:
            context ['lake'] = lake
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
    
class Weather (TemplateView):
    template_name = 'catches/weather.html'
    context_object_name = 'weather'

    def get_context_data(self, **kwargs): 
        context = super(Weather, self).get_context_data(**kwargs)
        current_weather = weather_data (Lake.objects.get (id=self.kwargs['pk']))

        context ['current'] = current_weather  #<class 'dict'>
        if current_weather != "":
            context ['current'] = current_weather  #<class 'dict'>
            context ['forecast'] = five_day_forcast (Lake.objects.get (id=self.kwargs['pk']))  #<class 'dict'>
        context ['lake'] = Lake.objects.get (id=self.kwargs['pk'])
        return context
    
class Weather2 (TemplateView):
    template_name = 'catches/weather2.html'
    context_object_name = 'weather'

    def get_context_data(self, **kwargs): 
        context = super(Weather2, self).get_context_data(**kwargs)
        lake = Lake.objects.get (id=self.kwargs['pk'])
        data = get_data (lake)
        context ['lake'] = lake
        context ['current']     = current (data)  #<class 'dict'>
        try:
            context ['temp_graph']  = temp_graph (data)  #<class 'graph'>
        except:
            context ['temp_graph'] = ""
        try:
            context ['forcast']     = hourly_forcast (data)  #<class 'dict'>
        except:
            context ['forcast'] = ""
        context ['daily']     = daily_forcast (data)  #<class 'dict'>
        # try:
        #     context ['daily']     = daily_forcast (data)  #<class 'dict'>
        # except:
        #     context ['daily'] = ""
        return context
        

class Plan(TemplateView):
    model = Lake
    template_name = 'catches/plan.html'
    context_object_name = 'lake'

    def get_context_data(self, **kwargs): 
        context = super(Plan, self).get_context_data(**kwargs)
        # current_week = int(timezone.now().strftime("%W"))
        week_obj = Week.objects.get (id= self.kwargs['wpk'])
        context ['lake'] = Lake.objects.get (id=self.kwargs['lpk'])
        context ['week'] = week_obj
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
        array_list = get_array(
            week = self.kwargs['wpk'], 
            lake = self.kwargs['lpk'], 
            temperature = get_hl (self.kwargs['wpk'])['low']
        )
        context ['array'] = array_list
        context ['ave_data'] = get_average_temp_for_week (week_obj.number)
        context ['fav'] = Lake.is_favorite (lake_pk = self.kwargs['lpk'], user_pk = self.request.user.id)
        return context
 
INFO_LIST = [
    {'tag': 'how-to-fish', 'title': 'How To Fish', 'description': 'How-to information', 
     'image': '/catches/site/Cardiff.jpeg'},
    {'tag': 'equipment', 'title': 'Equipment', 'description': 'Equipment specific information', 
     'image': 'catches/site/fly_rods.jpeg'},
    {'tag': 'technique', 'title': 'Technique', 'description': 'Different Techniques', 
     'image': 'catches/site/Cardiff_May_2022.jpeg'},
    {'tag': 'ice-out', 'title': 'Ice out', 'description': 'Fishing right after ice out', 
     'image': 'catches/site/Cardiff_April_2022.jpeg'},
    {'tag': 'spring', 'title': 'Spring fishing', 'description': 'Fishing in the spring', 
     'image': 'catches/site/Cardiff_May_2022_3.jpeg'},
    {'tag': 'fall', 'title': 'Fall fishing', 'description': 'Fall fishing', 
     'image': 'catches/site/Cardiff_May_2022_2.jpeg'},
    {'tag': 'heat', 'title': 'Fishing in the heat', 'description': 'How to fish in the heat', 
     'image': 'catches/site/Hay_lakes.jpeg'},
    {'tag': 'hatch', 'title': 'Hatch and Entomology', 'description': 'Hatch and Entomology', 
     'image': 'catches/site/dragon_nymph.jpeg'},
    {'tag': 'misc', 'title': 'Miscellaneous', 'description': 'Miscellaneous information', 
     'image': 'catches/site/Cardiff.jpeg'},
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
        context ['posts'] = Post.objects.filter (tags__name__contains = tag_detail)
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
    bug_results = Bug.objects.filter( Q(name__icontains=query)  | Q(static_tag__icontains=query))
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


class NotAllowed (TemplateView):
    template_name = '403.html'
