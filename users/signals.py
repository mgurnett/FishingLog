from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from catches.models import Region


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # 1. Handle profile creation, permissions, and initial region setup
        Profile.objects.create(user=instance)
        instance.groups.add(Group.objects.get(name='viewer'))
        region = Region (
            name = "My region",
            notes = "Lakes around your area",
            profile = instance.profile
        )
        region.save()

        # 2. 📨 Automatically notify the admin of the new registration
        subject = f"🎣 New Angler Registered: {instance.username}"
        message = (
            f"Hello Admin,\n\n"
            f"A new fly fisher has just registered an account on Stillwater Fly Fishing!\n\n"
            f"Username: {instance.username}\n"
            f"Email Address: {instance.email}\n"
            f"Date Joined: {instance.date_joined.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Tight lines,\n"
            f"Stillwater Platform Automation"
        )
        
        recipient_list = ['admin@stillwaterflyfishing.com','mgurnett@gmail.com'] 
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            # Prevents a mail server issue from interrupting the new user's signup flow
            print(f"Error sending registration notification email: {e}")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()