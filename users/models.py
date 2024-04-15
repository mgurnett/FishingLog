from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField (max_length=100, default = '10220 104 Ave NW')
    city = models.CharField (max_length=15, default = 'Edmonton')
    prov = models.CharField (max_length=5, default = 'AB')
    image = models.ImageField(default=static('default.jpg'), upload_to='profile_pics')
    # One-to-Many relationship with regions (a profile can have many regions)
    # regions = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property 
    def user_address (self):
        return f'{self.address}, {self.city}, {self.prov}' 

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
