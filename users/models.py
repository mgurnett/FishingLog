from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Address (models.Model):
    address = models.CharField (max_length=100, blank=True)
    city = models.CharField (max_length=15, blank=True)
    prov = models.CharField (max_length=5, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
