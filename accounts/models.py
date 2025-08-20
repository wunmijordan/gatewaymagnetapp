from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from guests.models import GuestEntry

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Team Member', 'Team Member'),
    ]

    TITLE_CHOICES = [
        ('Bro.', 'Bro.'),
        ('Min.', 'Min.'),
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Sis.', 'Sis.'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
    ]

    DEPARTMENT_CHOICES = [
        ('Crystal Sounds', 'Crystal Sounds'),
        ('Embassage', 'Embassage'),
        ('Expressions', 'Expressions'),
        ('Glitters', 'Glitters'),
        ('Green House', 'Green House'),
        ('Holy Police', 'Holy Police'),
        ('Media', 'Media'),
        ('Royal Guards', 'Royal Guards'),
        ('Temple Keepers', 'Temple Keepers'),
    ]

    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)

    # new fields
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, blank=True, null=True, default='Bro.')
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True, default='Single')
    department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES, blank=True, null=True, default='Crystal Sounds')
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'  # ← map to existing table

    def __str__(self):
        return self.full_name or f"User #{self.pk}"

    @property
    def initials(self):
        if self.full_name:
            return ''.join([name[0].upper() for name in self.full_name.split()[:2]])
        return self.username[0].upper() if self.username else "?"

    @property
    def guest_count(self):
        return GuestEntry.objects.filter(created_by=self).count()

