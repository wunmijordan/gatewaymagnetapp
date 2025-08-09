from django.contrib.auth.models import User
from django.db import models

def user_profile_upload_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number in international format, e.g. +1234567890")
    image = models.ImageField(upload_to=user_profile_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def initials(self):
        full_name = self.user.get_full_name()
        if full_name:
            return ''.join([name[0].upper() for name in full_name.split()])
        return self.user.username[0].upper()
