from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile only if it doesn't exist
        Profile.objects.get_or_create(user=instance)
    else:
        # Update the profile safely if it exists
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
# This signal handler ensures that a Profile instance is created or updated
# whenever a User instance is created or updated. It connects to the post_save