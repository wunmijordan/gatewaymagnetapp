from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile when a new User is created
        Profile.objects.create(user=instance)
    else:
        # For existing users, save the related profile if it exists
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # If no profile exists, create one (fallback)
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
