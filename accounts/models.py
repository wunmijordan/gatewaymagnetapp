from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.timezone import now
from django.conf import settings
from guests.models import GuestEntry
from django.utils import timezone
from datetime import datetime


CHURCH_COORDS = (6.641732871081892, 3.3706539797031843)  # (latitude, longitude)

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



class ChatMessage(models.Model):
  sender = models.ForeignKey(
      settings.AUTH_USER_MODEL,  # explicitly using CustomUser
      on_delete=models.CASCADE,
      related_name='sent_chats',
      db_index=True  # ⚡ faster sender lookups
  )
  parent = models.ForeignKey(
      'self',
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      related_name='replies',
      db_index=True  # ⚡ helps with threaded lookups
  )
  message = models.TextField(null=True, blank=True)
  voice_note = models.FileField(upload_to='chat_voice/', blank=True, null=True)
  guest_card = models.ForeignKey(
      GuestEntry,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='chat_messages',
      db_index=True  # ⚡ filter/pagination per guest
  )
  created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # ⚡ main pagination field
  #edited = models.BooleanField(default=False)
  #edited_at = models.DateTimeField(null=True, blank=True)
  #deleted = models.BooleanField(default=False)
  seen_by = models.ManyToManyField(
      settings.AUTH_USER_MODEL,  # explicitly using CustomUser
      related_name='seen_chats',
      blank=True
  )
  if settings.DEBUG:
      file = models.FileField(upload_to="chat/files/", blank=True, null=True)
  else:
      file = CloudinaryField("file", folder="chat/files", blank=True, null=True)
  file_type = models.CharField(max_length=100, blank=True, null=True)
  link_url = models.URLField(max_length=500, blank=True, null=True)
  link_title = models.CharField(max_length=255, blank=True, null=True)
  link_description = models.TextField(blank=True, null=True)
  link_image = models.URLField(max_length=500, blank=True, null=True)
  pinned = models.BooleanField(default=False, db_index=True)  # ⚡ faster queries for pinned
  pinned_at = models.DateTimeField(null=True, blank=True, db_index=True)
  pinned_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="pinned_messages"
  )

  def is_expired(self):
    """Convenience: check if pinned > 14 days ago"""
    if not self.pinned or not self.pinned_at:
        return False
    return (now() - self.pinned_at).days > 14


  class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),  # explicit index for ordering
            models.Index(fields=['sender', 'created_at']),  # ⚡ sender history
            models.Index(fields=['guest_card', 'created_at']),  # ⚡ per guest timeline
        ]

  def __str__(self):
      return f"Message #{self.id} by {self.sender.full_name or self.sender.username}"

  def is_seen_by_all(self):
      """Returns True if all users have seen this message"""
      from django.contrib.auth import get_user_model
      User = get_user_model()
      return self.seen_by.count() >= (User.objects.count() - 1)




class Event(models.Model):
  EVENT_TYPES = [
      ('Service', 'Service'),
      ('Followup', 'Guest Follow-up'),
      ('Meeting', 'Meeting'),
      ('Training', 'Training'),
      ('Other', 'Other'),
  ]

  ATTENDANCE_MODE_CHOICES = [
      ("Physical", "Physical"),
      ("Virtual", "Virtual"),
  ]

  name = models.CharField(max_length=255)
  event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
  day_of_week = models.CharField(
      max_length=20,
      choices=[
          ('Sunday', 'Sunday'),
          ('Monday', 'Monday'),
          ('Tuesday', 'Tuesday'),
          ('Wednesday', 'Wednesday'),
          ('Thursday', 'Thursday'),
          ('Friday', 'Friday'),
          ('Saturday', 'Saturday'),
      ],
      null=True,
      blank=True
  )
  attendance_mode = models.CharField(
      max_length=10,
      choices=ATTENDANCE_MODE_CHOICES,
      default="physical"
  )
  date = models.DateField(null=True, blank=True)  # floating events
  end_date = models.DateField(null=True, blank=True)  # optional for multi-day
  time = models.TimeField(null=True, blank=True)
  duration_days = models.PositiveIntegerField(default=1, help_text="Number of days this event lasts")
  is_recurring_weekly = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
  )

  class Meta:
      verbose_name = "Event"
      verbose_name_plural = "Events"
      ordering = ['date', 'day_of_week', 'time']

  def __str__(self):
      return f"{self.name} ({self.get_event_type_display()})"



class AttendanceRecord(models.Model):
  STATUS_CHOICES = [
      ('present', 'Present'),
      ('late', 'Late'),
      ('excused', 'Excused'),
      ('absent', 'Absent'),
  ]

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
  date = models.DateField(default=timezone.localdate)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
  remarks = models.TextField(blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
      unique_together = ('user', 'event', 'date')
      ordering = ['-date']

  def __str__(self):
      return f"{self.user} - {self.event.name} ({self.date})"


class PersonalReminder(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  date = models.DateField()
  time = models.TimeField(null=True, blank=True)
  is_done = models.BooleanField(default=False)

  class Meta:
      ordering = ['date', 'time']

  def __str__(self):
      return f"{self.user} - {self.title} ({self.date})"
  


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ("followup", "Follow-up"),
        ("message", "Message Sent"),
        ("guest_view", "Viewed Guest"),
        ("call", "Called Guest"),
        ("report", "Submitted Report"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    guest_id = models.CharField(max_length=50, blank=True, null=True)  # Optional
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "User Activities"

    def __str__(self):
        return f"{self.user} - {self.activity_type} ({self.created_at.strftime('%Y-%m-%d')})"
