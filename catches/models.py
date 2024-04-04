from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from PIL import Image
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
# from django.utils.text import slugify
import pandas as pd 
from django.contrib.auth.models import User 
from .fish_data import STRAIN_INFO, GENOTYPE_INFO, STRAIN, GENTOTYPE, STRENGTH, DISTRICTS
from users.models import Profile

class Week(models.Model):
    number = models.IntegerField()
    prev_num = models.IntegerField()
    next_num = models.IntegerField()

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
    def dates_in_week(self):
        yearnum = int(timezone.now().strftime("%Y"))
        start_date = f'{yearnum}/01/01'; end_date = f'{yearnum}/12/31'; 
        week_of_sundays = pd.date_range(start_date, end_date, freq='W-SUN')
        for wofs in week_of_sundays:
            week_num = wofs.strftime("%W")
            # print (f'yearnum is {yearnum} / Wnumber is {Wnumber} /week_num is {week_num} /')
            if int(week_num) == int(self.number):
                end_date = wofs + pd.DateOffset(6)
                week_info = {'week_num': week_num, 'start_date': wofs.strftime("%b %-d"), 'end_date': end_date.strftime("%b %-d")}
                return week_info
        return
              
class Fish(models.Model):
    name = models.CharField(max_length = 100)
    notes = RichTextField (blank=True, null=True)
    abbreviation = models.CharField (max_length=10, blank=True)    
    static_tag = models.SlugField()
    image = models.ImageField ('Picture of the bug', 
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

class Bug(models.Model):
    name = models.CharField ('Insect name', max_length=100)
    notes = RichTextField (blank=True, null=True)
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

class Lake(models.Model):
    name = models.CharField(max_length = 100)
    notes = RichTextField (blank=True, null=True)
    fish = models.ManyToManyField (Fish, through='Stock', blank=True)
    other_name = models.CharField (max_length=100, blank=True)
    ats = models.CharField (max_length=100, blank=True)
    lat = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    long = models.DecimalField (max_digits = 25, decimal_places=20, blank=True, null=True)
    # district = models.CharField (max_length=100, blank=True, choices = DISTRICTS)
    district = models.IntegerField (blank=True, null=True)
    waterbody_id = models.IntegerField (blank=True, null=True)
    favourite = models.BooleanField (default = False)
    static_tag = models.SlugField() 
    gps_url = models.URLField(max_length = 200, blank=True)
    
    class Meta:
        ordering = ['-favourite', 'name']

    @property 
    def num_of_stock (self):
        return self.fish.count

    @property 
    def num_of_hatch (self):
        return self.hatch_set.count

    @property 
    def lake_info (self):
        if self.favourite:
            fav="*"
        else:
            fav=""
        if self.other_name:
            output = f'{self.name} ({self.other_name}{fav})' 
        else:
            output = f'{self.name}{fav}' 
        return output   

    @property 
    def dist_name (self):
        dist = DISTRICTS[self.district][1]
        return dist 

    # https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django/8609425#8609425
    def __str__(self):
        if self.favourite:
            fav="*"
        else:
            fav=""
        if self.other_name == "":
            return f'{self.name}{fav} at {self.ats} of {self.dist_name}'
        else:
            return f'{self.name} ({self.other_name}{fav}) at {self.ats} of {self.dist_name}'  # used in the admin to set the name of the model
    
    #https://youtu.be/-s7e_Fy6NRU?t=1730
    def get_absolute_url (self):  #when you post a new lake, this then sets up to go look at the detail of that lake.
        return reverse ('lake_detail', kwargs = {'pk': self.pk})
    
class Region(models.Model):
    name = models.CharField (max_length=100)
    notes = models.TextField (blank=True)
    # Many-to-Many relationship with lakes (a region can have many lakes, and a lake can belong to many regions)
    lakes = models.ManyToManyField (to='Lake', blank=True)
    profile = models.ForeignKey (Profile, on_delete=models.CASCADE) 
    
    class Meta: 
        ordering = ['name']

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('region_list')
            
    @property 
    def lake_count (self):
        return Lake.objects.filter(region=self.id).count()

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
    notes = RichTextField (blank=True, null=True)
    deg = models.IntegerField ()
    direction = models.CharField(max_length = 10)

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('temp_list')
            
    @property 
    def log_count (self):
        return Log.objects.filter(temp=self.id).count()

class Fly_type(models.Model):
    name = models.CharField(max_length = 100)
    notes = RichTextField (blank=True, null=True)
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
    notes = RichTextField (blank=True, null=True)
    size_range = models.CharField ( max_length=100, blank=True)
    author = models.CharField (max_length=100, blank=True)
    static_tag = models.SlugField()
    snippet = models.CharField (max_length = 255, blank=True)
    image = models.ImageField ( 
        default='default.jpg', 
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
    temp = models.ForeignKey(Temp, blank=True, null=True, on_delete=models.SET_NULL)
    week = models.ForeignKey(Week, blank=True, null=True, on_delete=models.SET_NULL)
    catch_date = models.DateField(default=timezone.now)
    record_date = models.DateField(default=timezone.now) # another option is (auto_now_add = True)
    location = models.CharField (max_length=100, blank=True, null=True)
    length = models.FloatField ( blank=True, default=0.0 )
    weight = models.FloatField ( blank=True, default=0.0 )
    fly = models.ForeignKey(Fly, blank=True, null=True, on_delete=models.SET_NULL)
    fly_size = models.CharField (max_length=100, blank=True)
    fly_colour = models.CharField (max_length=100, blank=True)
    notes = RichTextField (blank=True, null=True)
    fish_swami = models.IntegerField (blank=True)
    num_landed = models.IntegerField (default=0)
    angler = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField (default = False)
     
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
            lake_name = self.lake.name + ' (' + self.lake.other_name + ')'
        else:
            lake_name = self.lake.name
        output = (f'{lake_name} a {self.fish.name} was caught with a {self.fly.name}')
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

class Hatch(models.Model):
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, blank=True, null=True, on_delete=models.SET_NULL)
    temp = models.ForeignKey(Temp, blank=True, null=True, on_delete=models.SET_NULL)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    notes = RichTextField (blank=True, null=True)
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
    notes = models.TextField (blank=True)
    author = models.CharField (max_length = 100, blank=True)
    url = models.URLField(max_length = 200, 
                    unique = True)
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
    notes = RichTextField (blank=True, null=True)
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
    notes = RichTextField (blank=True, null=True)
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

'''  
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
    # If True, the field is allowed to be blank. Default is False.
    # If blank=True then the field will not be required, whereas if it's False the field cannot be blank.

    # If True, Django will store empty values as NULL in the database. Default is False.
    # NULL - CharFields and TextFields are never saved as NULL. Blank values are stored in the DB as an empty string ('').
'''