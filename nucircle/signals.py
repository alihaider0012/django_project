from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile,following_list
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def signal (sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()
        following_list.objects.create(user=instance)   

    
