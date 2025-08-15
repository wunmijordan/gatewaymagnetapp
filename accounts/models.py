from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

def user_profile_upload_path(instance, filename):
    return f'profile_pics/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        # Defensive __str__ to never return None
        if self.full_name and self.user.username:
            return self.user.username
        return f"Profile #{self.pk} (No User)"

    @property
    def initials(self):
        full_name = self.user.get_full_name() if self.user else ""
        if full_name:
            return ''.join([name[0].upper() for name in full_name.split()])
        if self.user and self.user.username:
            return self.user.username[0].upper()
        return "?"

    @property
    def guest_count(self):
        from guests.models import GuestEntry
        return GuestEntry.objects.filter(created_by=self.user).count()
