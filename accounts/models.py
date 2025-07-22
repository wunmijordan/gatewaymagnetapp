from django.contrib.auth.models import User
from django.db import models

def user_profile_upload_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_profile_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create your models here.
