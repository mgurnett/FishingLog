from django.db import models
from django.urls import reverse
from PIL import Image

class Fly_type(models.Model):
    name = models.CharField(max_length = 100)
    notes = models.TextField(blank=True)

    def __str__(self):   
        return self.name


class Bug(models.Model):    
    name = models.CharField ('Insect name', max_length=100)
    description = models.TextField ('Description', blank=True)

    def __str__(self):   
        return self.name


class Fly(models.Model):
    name = models.CharField(max_length = 100)
    bug = models.ForeignKey(Bug, blank=True, null= True, on_delete=models.SET_NULL )
    fly_type = models.ForeignKey(Fly_type, blank=True, null= True, on_delete=models.SET_NULL) 
    description = models.CharField (max_length=400, blank=True)
    size_range = models.CharField ( max_length=100, blank=True)
    author = models.CharField (max_length=100, blank=True)
    tag_name = models.CharField(max_length = 100, blank=True)
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
        return reverse ('afly_detail', kwargs = {'pk': self.pk})
        

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