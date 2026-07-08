from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.templatetags.static import static
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# from ckeditor.fields import models.TextField
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image, ImageOps
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
# from django.utils.text import slugify
import pandas as pd 
from django.contrib.auth.models import User 
from catches.helpers.fish_data import *
from users.models import Profile
from blog.models import Post
import datetime

DEGREE_C = str(u"\u00b0" + "C")

class Week(models.Model):
    number = models.IntegerField()
    prev_num = models.IntegerField()
    next_num = models.IntegerField()
    ave_temp = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__ (self):
        return str(self.number)

    @property 
    def log_count (self):
        return self.log_set.count

    @property 
    def hatch_count (self):
        return self.hatch_set.count

    @property 
    def avereage_temp (self):
        return str(self.ave_temp) + DEGREE_C
    
    @property 
    def dates_in_week(self):
        yearnum = int(timezone.now().strftime("%Y"))
        start_date = f'{yearnum}/01/01'
        end_date = f'{yearnum}/12/31'
        week_of_sundays = pd.date_range(start_date, end_date, freq='W-SUN')
        for wofs in week_of_sundays:
            week_num = int(wofs.strftime("%W")) +1
            # print (f'yearnum is {yearnum} / Wnumber is {Wnumber} /week_num is {week_num} /')
            if week_num == int(self.number):
                end_date = wofs + pd.DateOffset(6)
                week_info = {'week_num': week_num, 'start_date': wofs.strftime("%b %-d"), 'end_date': end_date.strftime("%b %-d")}
                return week_info
        return
    
    # @property 
    # def dates_in_week(self):
    #     week_info_list = []
    #     yearnum = int(timezone.now().strftime("%Y"))
    #     start_date = f'{yearnum}/01/01'
    #     end_date = f'{yearnum}/12/31'
    #     week_of_sundays = pd.date_range(start_date, end_date, freq='W-SUN')
    #     for wofs in week_of_sundays:
    #         week_num = int(wofs.strftime("%W")) + 1
    #         end_date = wofs + pd.DateOffset(6)
    #         week_info = {'week_num': week_num, 'start_date': wofs.strftime("%b %-d"), 'end_date': end_date.strftime("%b %-d")}
    #         week_info_list.append (week_info)
    #     return week_info_list
              
class Fish(models.Model):
    name = models.CharField(max_length = 100)
    notes = CKEditor5Field (blank=True, null=True)
    abbreviation = models.CharField (max_length=10, blank=True)    
    static_tag = models.SlugField()
    image = models.ImageField ('Picture of the fish', 
        default=None, 
        upload_to='fish/', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        blank=True, null=True
        )
 
    def save(self, *args, **kwargs):
        super(Fish, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.abbreviation})'  # used in the admin to set the name of the model
    
    def get_absolute_url (self):  
        return reverse ('fish_detail', kwargs = {'pk': self.pk})

    @property 
    def num_of_vids (self):
        return Video.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_pics (self):
        return Picture.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_arts (self):
        return Article.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_posts (self):
        return Post.objects.filter (tags__name__contains=self.static_tag).count

class Bug(models.Model):
    name = models.CharField ('Insect name', max_length=100)
    notes = CKEditor5Field (blank=True, null=True)
    static_tag = models.SlugField()
    image = models.ImageField ('Picture of the bug', 
        default=None, 
        upload_to='bug/', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        )

    def save(self, *args, **kwargs):
        super(Bug, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url (self):
        return reverse ('bug_detail', kwargs = {'pk': self.pk})
            
    @property 
    def fly_ent_count (self):
        return Fly.objects.filter(bug=self.id).count()
            
    @property 
    def fly_kind_count (self):
        return Fly.objects.filter(fly_type=self.id).count()

    @property 
    def num_of_vids (self):
        return Video.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_pics (self):
        return Picture.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_arts (self):
        return Article.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_posts (self):
        return Post.objects.filter (tags__name__contains=self.static_tag).count

class Lake(models.Model):
    name = models.CharField(max_length = 100)
    notes = CKEditor5Field (blank=True, null=True)
    fish = models.ManyToManyField (Fish, through='Stock', blank=True)
    other_name = models.CharField (max_length=100, blank=True)
    ats = models.CharField (max_length=100, blank=True)
    reg_location = models.CharField (max_length=100, blank=True)
    lat = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    long = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    # district = models.CharField (max_length=100, blank=True, choices = DISTRICTS)
    district = models.IntegerField (blank=True, null=True)
    waterbody_id = models.IntegerField (blank=True, null=True)
    # favourite = models.BooleanField (default = False)
    static_tag = models.SlugField() 
    gps_url = models.URLField(max_length = 200, blank=True)
    size = models.FloatField (blank=True, null=True)
    
    class Meta:
        ordering = ['name']

    @property 
    def num_of_stock (self):
        return self.fish.count

    @property 
    def num_of_hatch (self):
        return self.hatch_set.count

    @property 
    def num_of_vids (self):
        return Video.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_pics (self):
        return Picture.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_arts (self):
        return Article.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_posts (self):
        return Post.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def lake_info (self):
        if self.other_name:
            output = f'{self.name} ({self.other_name})' 
        else:
            output = f'{self.name}' 
        return output   

    @property 
    def lake_full_name (self):
        if self.other_name:
            output = f'{self.name} ({self.other_name}) - {self.reg_location}' 
        else:
            output = f'{self.name} - {self.reg_location}' 
        return output 

    @property 
    def dist_name(self):
        # 1. Handle cases where district is None/Null in the database
        if self.district is None:
            return "Unknown District"
            
        # 2. Safely look up the display name from the DISTRICTS tuple/list
        # This converts DISTRICTS to a dictionary for key-value lookup,
        # fallback to the raw number if the key isn't found.
        return dict(DISTRICTS).get(self.district, f"District {self.district}")

    @property 
    def kml_tooltip (self):
        return KML_TOOLTIP

    # https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django/8609425#8609425
    def __str__(self):
        if self.other_name == "":
            # return f'{self.name} at {self.ats} of {self.dist_name}'
            return f'{self.name} of {self.dist_name} in {self.reg_location}'
        else:
            # return f'{self.name} ({self.other_name}) at {self.ats} of {self.dist_name}'
            return f'{self.name} ({self.other_name}) of {self.dist_name} in {self.reg_location}'
    
    #https://youtu.be/-s7e_Fy6NRU?t=1730
    def get_absolute_url (self):  #when you post a new lake, this then sets up to go look at the detail of that lake.
        return reverse ('lake_detail', kwargs = {'pk': self.pk})
    
class Region(models.Model):
    name = models.CharField(max_length=100)
    notes = CKEditor5Field(blank=True, null=True)
    lakes = models.ManyToManyField(to='Lake', blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=25, blank=True)
    prov = models.CharField(max_length=5, blank=True)

    def save(self, *args, **kwargs):
        # Check if fields are empty before saving, and populate from the profile
        if not self.address and self.profile:
            self.address = self.profile.address
        if not self.city and self.profile:
            self.city = self.profile.city
        if not self.prov and self.profile:
            self.prov = self.profile.prov
            
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:  
        ordering = ['name']

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('region_list')
            
    @property 
    def lake_count (self):
        return Lake.objects.filter(region=self.id).count()

    @property 
    def kml_tooltip (self):
        return KML_TOOLTIP

class Stock(models.Model):
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    date_stocked = models.DateField()
    number = models.IntegerField ()
    length = models.FloatField ()
    # length = models.FloatField (max_digits = 10, decimal_places=2)
    strain = models.CharField (
        max_length=100, 
        blank=True,
        choices = STRAIN,
        )
    gentotype = models.CharField (
        max_length=100, 
        blank=True,
        choices = GENTOTYPE,
        )
    
    class Meta:
        ordering = ['-date_stocked']

    def get_absolute_url (self):
        return reverse ('stock_list')

    @property 
    def inch (self):
        return round (float(self.length) * .393701,1)

    def __str__(self):
        return f'Stocking report: On {self.date_stocked} at {self.lake}, {self.number} ({self.length}cm or {self.inch}inch) {self.fish} ({self.strain}/{self.gentotype}) were stocked'

        # https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types
        #https://youtu.be/-HuTlmEVOgU - viedo on mant to many relationship

        # Payne Lake  Mami Lake  NE10 -2-28-W4 RNTR  Beitty Resort  3N 14.2 38,000  21-Sep-22

    @property 
    def full_geno (self):
        geno_list = []
        for i in GENTOTYPE:
            geno_list.append(i[0])

        geno_index = geno_list.index(self.gentotype)
        geno_found = GENTOTYPE[geno_index][1]

        return geno_found

    @property 
    def full_strain (self):
        strain_list = []
        for i in STRAIN:
            strain_list.append(i[0])

        strain_index = strain_list.index(self.strain)
        strain_found = STRAIN[strain_index][1]

        return strain_found

    @property 
    def geno_tooltip (self):
        return GENOTYPE_INFO

    @property 
    def strain_tooltip (self):
        return STRAIN_INFO

class Temp(models.Model):
    name = models.CharField(max_length = 100)
    search_keys = models.CharField(max_length = 400, blank=True)
    week = models.ManyToManyField (Week, blank=True)
    notes = CKEditor5Field (blank=True, null=True)
    deg = models.IntegerField ()
    direction = models.CharField(max_length = 10)

    def __str__ (self):
        return f'{self.name}'

    def get_absolute_url (self):
        return reverse ('temp_list')
            
    @property 
    def log_count (self):
        return Log.objects.filter(temp=self.id).count()

class Fly_type(models.Model):
    name = models.CharField(max_length = 100)
    notes = CKEditor5Field (blank=True, null=True)
    image = models.ImageField ('Picture of fly type', 
        default=None, 
        upload_to='fly_type/', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        )
 
    def save(self, *args, **kwargs):
        super(Fly_type, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path) 

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('fly_type_detail', kwargs = {'pk': self.pk})
            
    @property 
    def fly_kind_count (self):
        return Fly.objects.filter(fly_type=self.id).count()

class Fly(models.Model):
    name = models.CharField(max_length = 100)
    bug = models.ForeignKey(Bug, blank=True, null= True, on_delete=models.SET_NULL )
    fly_type = models.ForeignKey(Fly_type, blank=True, null= True, on_delete=models.SET_NULL) 
    notes = CKEditor5Field (blank=True, null=True)
    size_range = models.CharField ( max_length=100, blank=True)
    author = models.CharField (max_length=100, blank=True)
    static_tag = models.SlugField()
    snippet = models.CharField (max_length = 255, blank=True)
    image = models.ImageField ( 
        default='flys/default_fly.jpg', 
        upload_to='flys/', 
        height_field=None, 
        width_field=None, 
        max_length=100,
        blank=True)
 
    class Meta:
        ordering = ['fly_type','name']

    def __str__(self):
        if self.bug:
            bug = self.bug.name
        else:
            bug="" 
        if self.fly_type:
            ftype = self.fly_type.name
        else:
            ftype=""   
        return f'{self.name} - {bug} {ftype}'  # used in the admin to set the name of the model

    def get_absolute_url (self):  
        return reverse ('fly_detail', kwargs = {'pk': self.pk})
        
    @property 
    def tag_title (self):
        return self.tag_name

    @property 
    def num_of_vids (self):
        return Video.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_pics (self):
        return Picture.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_arts (self):
        return Article.objects.filter (tags__name__contains=self.static_tag).count

    @property 
    def num_of_posts (self):
        return Post.objects.filter (tags__name__contains=self.static_tag).count

    def save(self, *args, **kwargs):
        super(Fly, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path) 

class Log(models.Model):  
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE) 
    fish = models.ForeignKey(Fish, blank=True, null=True, on_delete=models.SET_NULL)
    temp = models.ForeignKey(Temp, default = 1, on_delete=models.SET_DEFAULT)
    week = models.ForeignKey(Week, blank=True, null=True, on_delete=models.SET_NULL)
    # Change catch_date default from timezone.now to local today:
    catch_date = models.DateField(default=datetime.date.today)
    # Change record_date default as well:
    record_date = models.DateField(default=datetime.date.today)
    catch_time = models.TimeField(blank=True, null=True, default=timezone.now)
    location = models.CharField (max_length=100, blank=True, null=True)
    length = models.FloatField ( blank=True, default=0.0 )
    weight = models.FloatField ( blank=True, default=0.0 )
    fly = models.ForeignKey(Fly, blank=True, null=True, on_delete=models.SET_NULL)
    fly_size = models.CharField (max_length=100, blank=True)
    fly_colour = models.CharField (max_length=100, blank=True)
    notes = CKEditor5Field (blank=True, null=True)
    fish_swami = models.IntegerField (blank=True)
    num_landed = models.IntegerField (default=0)
    angler = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField (default = False)
    lake_depth = models.FloatField (blank=True, null=True)
    gps_lat = models.FloatField (blank=True, null=True)
    gps_long = models.FloatField (blank=True, null=True)
    catch_depth = models.FloatField (blank=True, null=True)
    

    class Meta:
        ordering = ['temp']

    def get_absolute_url (self):
        return reverse('log_detail', kwargs={'pk': self.pk})

    def __str__(self):
        if self.lake.other_name:
            lake_name = self.lake.name + ' (' + self.lake.other_name + ')'
        else:
            lake_name = self.lake.name
        if self.fly:
            output = (f'On {self.catch_date} at {lake_name} a {self.fish.name} was caught with a {self.fly.name}')
        else:
            output = (f'On {self.catch_date} at {lake_name} a temperature was recorded')
        return output

    @property 
    def len_inch (self):
        return round (self.length * .393701,1)

    @property 
    def wen_lbs (self):
        return round (self.weight * 2.204623,1)

    @property 
    def card_top (self):
        if self.lake.other_name:
            lake_name = (f'{self.lake.name} ({self.lake.other_name})')
        else:
            lake_name = self.lake.name
        if self.fly:
            fly_name = (f' was caught with a {self.fly.name}')
        else:
            fly_name = ''
        if self.fish:
            fish_name = (f' a {self.fish.name}')
        else:
            fish_name = ''
        output = (f'{lake_name} {fish_name} {fly_name}')
        return output

    @property 
    def fish_info (self):
        if self.length:
            len_out = f' (length: {self.length}cm ({self.len_inch}")' 
        else:
            len_out = ""
        if self.weight:
            wen_out = f' (weight: {self.weight}kg ({self.wen_lbs}lbs)' 
        else:
            wen_out = ""
        output = (f'{self.fish.name} {len_out} {wen_out}')
        return output

    @property 
    def fly_info (self):
        if self.fly_colour and self.fly_size:
            return f'{self.fly.name} ({self.fly_colour} #{self.fly_size})'
        if self.fly_colour and not self.fly_size:
            return f'{self.fly.name} ({self.fly_colour})'
        if not self.fly_colour and self.fly_size:
                return f'{self.fly.name} (#{self.fly_size})' 
        if not self.fly_colour and not self.fly_size:
            return self.fly.name
        return self.fly.name

    # @property 
    # def num_of_logs (self):
    #     return self.angler_set.count

    def save(self, *args, **kwargs):
        if not self.week:
            week_num = Week.objects.get(number=int(self.catch_date.strftime('%U')))
            self.week = week_num
        super().save(*args, **kwargs)

class LogWeather(models.Model):
    log = models.OneToOneField(Log, on_delete=models.CASCADE, related_name='weather')
    temp = models.FloatField(blank=True, null=True)
    feels_like = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    clouds = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_deg = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=20, blank=True)

def __str__(self):
    if self.log_id and hasattr(self, 'log') and self.log:
        return f"Weather for Log {self.log.id}"
    return f"Weather for Log (Deleted or Missing ID: {self.log_id})"

class Hatch(models.Model):
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, blank=True, null=True, on_delete=models.SET_NULL)
    temp = models.ForeignKey(Temp, blank=True, null=True, on_delete=models.SET_NULL)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    notes = CKEditor5Field (blank=True, null=True)
    static_tag = models.SlugField()
    sight_date = models.DateField(default=timezone.now)
     
    class Meta:
        ordering = ['week']

    def __str__ (self):
        return f'bug: {self.bug.name} at lake: {self.lake.name}'

    def get_absolute_url (self):
        return reverse ('hatch_detail', kwargs = {'pk': self.pk})

    def save (self, *args, **kwargs):
        if not self.week:
            week_num = Week.objects.get(number = int(self.sight_date.strftime('%U')))
            self.week = week_num
        super().save (*args, **kwargs)
 
class Video(models.Model):
    name = models.CharField(max_length = 100)
    notes = CKEditor5Field (blank=True, null=True)
    author = models.CharField (max_length = 100, blank=True)
    url = models.URLField(max_length = 200, unique = True)
    date_added = models.DateField(default=timezone.now)
    tags = TaggableManager(blank=True)
    snippet = models.CharField (max_length = 255, blank=True)
    
    class Meta:
        ordering = ['-date_added']

    def __str__ (self):
        if self.snippet:
            snip = f" - {self.snippet}"
        else:
            snip=""
        if self.author:
            auth = f" - by: {self.author.title()}"
        else:
            auth=""
        if self.tags:
            t_list = f' tags ({u", ".join(o.name for o in self.tags.all())})'
        return f'{self.name.title()}{snip}{auth}{t_list}'

    def get_absolute_url (self):
        return reverse ('video_detail', kwargs = {'pk': self.pk})

    @property
    def tag_list (self):
        t_list = u", ".join(o.name for o in self.tags.all())
        return str(t_list)
    
class Article(models.Model):
    name = models.CharField(max_length = 100)
    author = models.CharField (max_length = 100, blank=True)
    url = models.URLField(max_length = 200, blank=True)
    notes = CKEditor5Field (blank=True, null=True)
    file = models.FileField( upload_to='files/', blank=True )
    date_added = models.DateField(default=timezone.now)
    tags = TaggableManager(blank=True)
    snippet = models.CharField (max_length = 255, blank=True)
    
    class Meta:
        ordering = ['-date_added']

    def __str__ (self):
        if self.snippet:
            snip = f" - {self.snippet}"
        else:
            snip=""
        if self.author:
            auth = f" - by: {self.author.title()}"
        else:
            auth=""
        if self.tags:
            t_list = f' tags ({u", ".join(o.name for o in self.tags.all())})'
        return f'{self.name.title()}{snip}{auth}{t_list}'

    def get_absolute_url (self):
        return reverse ('article_detail', kwargs = {'pk': self.pk})

    @property
    def tag_list (self):
        t_list = u", ".join(o.name for o in self.tags.all())
        return str(t_list)
     
class Picture(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField( upload_to='pictures/', blank=True )
    notes = CKEditor5Field (blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    tags = TaggableManager(blank=True)
    snippet = models.CharField (max_length = 255, blank=True)
    
    class Meta:
        ordering = ['-date_added']

    def __str__ (self):
        if self.snippet:
            snip = f" - {self.snippet}"
        else:
            snip=""
        if self.tags:
            t_list = f' tags ({u", ".join(o.name for o in self.tags.all())})'
        return f'{self.name.title()}{snip}{t_list}'

    def get_absolute_url (self):
        return reverse ('picture_detail', kwargs = {'pk': self.pk})

    @property
    def tag_list (self):
        t_list = u", ".join(o.name for o in self.tags.all())
        return str(t_list)

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        img = ImageOps.exif_transpose(img)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)  
    
class Chart(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="week")
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="insect")
    strength = models.IntegerField ( 
        default = 0,
        choices = STRENGTH,
        )

    def __str__ (self):
        return f'bug: {self.bug.name} in week: {self.week.number} has a strength of: {self.strength}'

    @property 
    def strength_name (self):
        strength_list = []
        for i in STRENGTH:
            strength_list.append(i[0])

        strength_index = strength_list.index(self.strength)
        strength_found = STRENGTH[strength_index][1]

        return strength_found

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # users = models.ManyToManyField (to='User', blank=True)
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    # lakes = models.ManyToManyField (to='Lake', blank=True)
    date_added = models.DateField(auto_now_add = True)
    new_flag = models.DateField(auto_now_add = True)
    
    class Meta: 
        ordering = ['lake']
         
    @property 
    def is_favorite (lake_pk,  user_pk):
        print (f'{lake_pk = } {user_pk = }')
        try:
            fav = Favorite.objects.get(lake=lake_pk, user=user_pk)
        except:
            return False
        else:
            return True

    def __str__ (self):
        return self.lake.name

    def get_absolute_url (self):
        return reverse ('favorite_list')

class Announcment(models.Model):
    lake_id = models.IntegerField (default = 0)
    notes = models.TextField (blank=True)
    
    class Meta: 
        ordering = ['notes']

    def __str__ (self):
        return f'{self.notes} ({self.lake_id})' 

    def get_absolute_url (self):
        return reverse ('catch_home')

'''  On Delete
ON DELETE CASCADE: if a row of the referenced table is deleted, then all matching rows 
in the referencing table are deleted.
ON DELETE SET NULL: if a row of the referenced table is deleted, then all referencing columns 
in all matching rows of the referencing table to be set to null.
on_delete=models.SET_NULL, null=True)
ON DELETE SET DEFAULT: if a row of the referenced table is deleted, then all referencing 
columns in all matching rows of the referencing table to be set to the column’s default value.
on_delete=models.SET_DEFAULT, default=1)
ON DELETE RESTRICT: it is prohibited to delete a row of the referenced table if that row 
has any matching rows in the referencing table.
ON DELETE NO ACTION (the default): there is no referential delete action; the referential 
constraint only specifies a constraint check.
NO DELETE PROTECT
'''

''' blank talks about being required!!!!!!!  
    # 
'''


@receiver(post_save, sender=Log)
def fetch_weather_for_log(sender, instance, created, **kwargs):
    if hasattr(instance, 'weather'):
        return

    if instance.gps_lat and instance.gps_long and instance.catch_date and instance.catch_time:
        import datetime
        from django.utils.timezone import make_aware
        from catches.helpers.Open_Weather import get_historical_weather
        
        dt = datetime.datetime.combine(instance.catch_date, instance.catch_time)
        try:
            dt_aware = make_aware(dt)
        except ValueError:
            dt_aware = dt
        unix_timestamp = int(dt_aware.timestamp())
        
        data = get_historical_weather(instance.gps_lat, instance.gps_long, unix_timestamp)
        if data and 'data' in data and len(data['data']) > 0:
            w_data = data['data'][0]
            LogWeather.objects.create(
                log=instance,
                temp=w_data.get('temp'),
                feels_like=w_data.get('feels_like'),
                pressure=w_data.get('pressure', 0) / 10 if w_data.get('pressure') else None,
                humidity=w_data.get('humidity'),
                clouds=w_data.get('clouds'),
                wind_speed=w_data.get('wind_speed'),
                wind_deg=w_data.get('wind_deg'),
                description=w_data.get('weather', [{}])[0].get('description', '') if w_data.get('weather') else '',
                icon=w_data.get('weather', [{}])[0].get('icon', '') if w_data.get('weather') else ''
            )

    # If True, the field is allowed to be blank. Default is False.
    # If blank=True then the field will not be required, whereas if it's False the field cannot be blank.

    # If True, Django will store empty values as NULL in the database. Default is False.
    # NULL - CharFields and TextFields are never saved as NULL. Blank values are stored in the DB as an empty string ('').
