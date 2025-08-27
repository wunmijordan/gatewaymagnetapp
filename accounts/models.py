from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from guests.models import GuestEntry


class CustomUser(AbstractUser):
  ROLE_CHOICES = [
    ('Superuser', 'Superuser'),
    ('Admin', 'Admin'),
    ('Message Manager', 'Message Manager'),
    ('Registrant', 'Registrant'),
    ('Team Member', 'Team Member'),
  ]

  TITLE_CHOICES = [
    ('Bro.', 'Bro.'), ('Min.', 'Min.'), ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'), ('Sis.', 'Sis.'),
  ]

  MARITAL_STATUS_CHOICES = [('Married', 'Married'), ('Single', 'Single')]

  DEPARTMENT_CHOICES = [
    ('Crystal Sounds', 'Crystal Sounds'), ('Embassage', 'Embassage'), ('Expressions', 'Expressions'),
    ('Glitters', 'Glitters'), ('Green House', 'Green House'), ('Holy Police', 'Holy Police'),
    ('Magnet', 'Magnet'), ('Media', 'Media'), ('Minister', 'Minister'),
    ('Pastor', 'Pastor'), ('Royal Guards', 'Royal Guards'), ('Temple Keepers', 'Temple Keepers'),
  ]

  full_name = models.CharField(max_length=255, blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)
  image = CloudinaryField('image', blank=True, null=True)
  title = models.CharField(max_length=50, choices=TITLE_CHOICES, blank=True, null=True)
  marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
  department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  date_of_birth = models.CharField(max_length=50, blank=True, null=True)
  is_online = models.BooleanField(default=False)
  role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Team Member')


  def __str__(self):
    return self.full_name or f"User #{self.pk}"

  @property
  def initials(self):
    if self.full_name:
      return ''.join([name[0].upper() for name in self.full_name.split()[:2]])
    return self.username[0].upper() if self.username else "?"

  @property
  def guest_count(self):
    return self.assigned_guests.count() if hasattr(self, 'assigned_guests') else 0