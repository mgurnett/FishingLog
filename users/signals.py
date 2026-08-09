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

        # 3. 📨 Send a welcome email to the new user
        user_subject = "Welcome to Stillwater Fly Fishing!"
        user_message = (
            f"Hi {instance.username},\n\n"
            f"Welcome to the StillwaterFlyFishing.com community! We're glad to have you join us.\n\n"
            f"This site is dedicated to the unique challenges and rewards of stillwater angling in the lakes of Alberta, and we're excited to have another voice in the mix. To help us get to know our members a little better, we'd love to hear a bit from you:\n\n"
            f"How did you find out about the site? (Word of mouth, search, social media, etc.)\n\n"
            f"What part of the province do you call home? Knowing where everyone is based helps us understand which waters are being discussed most.\n\n"
            f"As you start exploring and participating, we just ask that you keep a few things in mind: please respect the site and the people who use it. We aim to keep this a helpful, welcoming, and constructive environment for fly fishers of all skill levels.\n\n"
            f"If you would like to contribute to the site with things like logs, hatch sightings and pictures, please reach out to admin@StillwaterFlyFishing.com and we can add you to the contributors list.\n\n"
            f"Tight lines,\n\n"
            f"Michael for The StillwaterFlyFishing.com Team"
        )
        try:
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending welcome email to user: {e}")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()