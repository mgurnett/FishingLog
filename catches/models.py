from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image

''' blank talks about being required!!!!!!!  
    # 
    # If True, the field is allowed to be blank. Default is False.
    # If blank=True then the field will not be required, whereas if it's False the field cannot be blank.

    # If True, Django will store empty values as NULL in the database. Default is False.
    # NULL - CharFields and TextFields are never saved as NULL. Blank values are stored in the DB as an empty string ('').
'''

STRAIN = (
    ("BEBE", "Beitty x Beitty"),
    ("BRBE", "Bow River x Beitty"),
    ("CLCL", "Campbell Lake"),
    ("LYLY", "Lyndon"),
    ("PLPL", "Pit Lake"),
    ("TLTLJ", "Trout Lodge / Jumpers"),
    ("TLTLK", "Trout Lodge / Kamloops"),
    ("TLTLS", "Trout Lodge / Silvers"),
    ("LSE", "Lac Ste. Anne"),
    ("JBL", "Job Lake"),
)

GENTOTYPE = (
    ("2N", "diploid"),
    ("3N", "triploid"),
    ("AF2N", "all-female diploid"),
    ("AF3N", "all-female triploid"),
)

class Region(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField (blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('region_list')
        
class Fish(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField( blank=True )
    abbreviation = models.CharField (max_length=10, blank=True)
    image = models.ImageField (default='default.jpg', upload_to='', height_field=None, width_field=None, max_length=100, blank=True)     
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.abbreviation})'  # used in the admin to set the name of the model
    
    def get_absolute_url (self):  
        return reverse ('fish_detail', kwargs = {'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Fish, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path) 

class Bug(models.Model):    
    name = models.CharField ('Insect name', max_length=100)
    description = models.TextField ('Description', blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url (self):
        return reverse ('bug_list')

class Lake(models.Model):
    name = models.CharField(max_length = 100)
    region = models.ForeignKey(Region, blank=True, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    fish = models.ManyToManyField (Fish, through='Stock', blank=True)
    other_name = models.CharField (max_length=100, blank=True)
    ats = models.CharField (max_length=100, blank=True)
    lat = models.DecimalField (max_digits = 15, decimal_places=10, blank=True, null=True)
    long = models.DecimalField (max_digits = 15, decimal_places=10, blank=True, null=True)
    district = models.CharField (max_length=100, blank=True)
    waterbody_id = models.IntegerField (blank=True, null=True)
    favourite = models.BooleanField (default = False)
    
    class Meta:
        ordering = ['-favourite', 'name']

    @property 
    def num_of_stock (self):
        return self.fish.count

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

# https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django/8609425#8609425
    def __str__(self):
        if self.favourite:
            fav="*"
        else:
            fav=""
        if self.other_name == "":
            return f'{self.name}{fav} at {self.ats}'
        else:
            return f'{self.name} ({self.other_name}{fav}) at {self.ats}'  # used in the admin to set the name of the model
    
    #https://youtu.be/-s7e_Fy6NRU?t=1730
    def get_absolute_url (self):  #when you post a new lake, this then sets up to go look at the detail of that lake.
        return reverse ('lake_detail', kwargs = {'pk': self.pk})

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
        return round (self.length * .393701,1)

    def __str__(self):
        return f'Stocking report: On {self.date_stocked} at {self.lake}, {self.number} ({self.length}cm or {self.inch}inch) {self.fish} were stocked'

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

class Temp(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField(blank=True)

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('temp_list')

class Fly_type(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField(blank=True)

    def __str__ (self):
        return self.name

    def get_absolute_url (self):
        return reverse ('fly_type_list')

class Fly(models.Model):
    name = models.CharField(max_length = 100)
    bug = models.ForeignKey(Bug, blank=True, null= True, on_delete=models.SET_NULL )
    fly_type = models.ForeignKey(Fly_type, blank=True, null= True, on_delete=models.SET_NULL) 
    description = models.CharField (max_length=400, blank=True)
    size_range = models.CharField ( max_length=100, blank=True)
    author = models.CharField (max_length=100, blank=True)
    youtube = models.URLField (blank=True )
    image = models.ImageField ( 
        default='default.jpg', 
        upload_to='', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.description}'  # used in the admin to set the name of the model

    def get_absolute_url (self):  
        return reverse ('fly_list')

    def save(self, *args, **kwargs):
        super(Fly, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path) 
            img.save(self.image.path)

class Log(models.Model):
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    temp = models.ForeignKey(Temp, blank=True, on_delete=models.CASCADE)
    fly = models.ForeignKey(Fly, blank=True, on_delete=models.CASCADE)    
    catch_date = models.DateField(default=timezone.now)
    record_date = models.DateField(default=timezone.now)
    location = models.CharField (max_length=100, blank=True)
    length = models.FloatField ( blank=True, null=True)
    weight = models.FloatField ( blank=True, null=True)
    fly = models.ForeignKey(Fly, on_delete=models.CASCADE)
    fly_size = models.CharField (max_length=100, blank=True)
    fly_colour = models.CharField (max_length=100, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField ('Picture of fly', 
        default=None, 
        upload_to='', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        blank=True
        )
     
    class Meta:
        ordering = ['temp']

    def get_absolute_url (self):
        return reverse ('logs_list')

    def __str__(self):
        if self.lake.other_name:
            lake_name = self.lake.name + ' (' + self.lake.other_name + ')'
        else:
            lake_name = self.lake.name
        output = (f'On {self.catch_date} at {lake_name} a {self.fish.name} was caught with a {self.fly.name}')
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

class Bug_site(models.Model):
    name =  models.CharField(max_length = 100)
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)
    temp = models.ForeignKey(Temp, blank=True, on_delete=models.CASCADE)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
     
    class Meta:
        ordering = ['temp']

    def __str__ (self):
        return self.name


    def get_absolute_url (self):
        return reverse ('bug_site_list')

