import re
from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from cloudinary.models import CloudinaryField


User = get_user_model()

class GuestEntry(models.Model):

    TITLE_CHOICES = [
        ('Chief', 'Chief'),
        ('Dr.', 'Dr.'),
        ('Engr.', 'Engr.'),
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Ms.', 'Ms.'),
        ('Pastor', 'Pastor'),
        ('Prof.', 'Prof.'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Not Stated', 'Not Stated'),
    ]

    PURPOSE_CHOICES = [
        ('Home Church', 'Home Church'),
        ('Occasional Visit', 'Occasional Visit'),
        ('One-Time Visit', 'One-Time Visit'),
        ('Special Programme Visit', 'Special Programme Visit'),
        ('Not Stated', 'Not Stated'),
    ]

    CHANNEL_CHOICES = [
        ('Billboard (Grammar School)', 'Billboard (Grammar School)'),
        ('Billboard (Kosoko)', 'Billboard (Kosoko)'),
        ('Billboard (Ojodu)', 'Billboard (Ojodu)'),
        ('Facebook', 'Facebook'),
        ('Flyer', 'Flyer'),
        ('Instagram', 'Instagram'),
        ('Referral', 'Referral'),
        ('Self', 'Self'),
        ('Visit', 'Visit'),
        ('YouTube', 'YouTube'),
        ('Not Stated', 'Not Stated'),
    ]

    SERVICE_CHOICES = [
        ('Black Ball', 'Black Ball'),
        ('Breakthrough Campaign', 'Breakthrough Campaign'),
        ('Breakthrough Festival', 'Breakthrough Festival'),
        ('Code Red. Revival', 'Code Red. Revival'),
        ('Cross Over', 'Cross Over'),
        ('Deep Dive', 'Deep Dive'),
        ('Family Hangout', 'Family Hangout'),
        ('Forecasting', 'Forecasting'),
        ('Life Masterclass', 'Life Masterclass'),
        ('Love Lounge', 'Love Lounge'),
        ('Midweek Recharge', 'Midweek Recharge'),
        ('Outreach', 'Outreach'),
        ('Praise Party', 'Praise Party'),
        ('Quantum Leap', 'Quantum Leap'),
        ('Recalibrate Marathon', 'Recalibrate Marathon'),
        ('Singles Connect', 'Singles Connect'),
        ('Supernatural Encounter', 'Supernatural Encounter'),
    ]

    STATUS_CHOICES = [
        ('Select Status', 'Select Status'),
        ('Planted', 'Planted'),
        ('Planted Elsewhere', 'Planted Elsewhere'),
        ('Relocated', 'Relocated'),
        ('Work in Progress', 'Work in Progress'),
    ]

    SOCIAL_MEDIA_CHOICES = [
        ('Whatsapp', 'WhatsApp'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Tiktok', 'Tiktok'),
    ]

    picture = CloudinaryField('image', blank=True, null=True)

    @property
    def initials(self):
        if self.full_name:
            return ''.join([n[0].upper() for n in self.full_name.split()[:2]])
        return 'G'

    custom_id = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES, blank=True, default='Mr.')
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    phone_number = models.CharField(max_length=20, blank=True, null= True)
    email = models.EmailField(blank=True)
    date_of_birth = models.CharField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, default='Single')
    home_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    date_of_visit = models.DateField(default=localdate)
    purpose_of_visit = models.CharField(max_length=30, choices=PURPOSE_CHOICES, blank=True, default='Home Church')
    channel_of_visit = models.CharField(max_length=30, choices=CHANNEL_CHOICES, blank=True, default='Referral')
    service_attended = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, default='Love Lounge')
    referrer_name = models.CharField(max_length=100, blank=True)
    referrer_phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Select Status')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_guests')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_guests')


    def save(self, *args, **kwargs):
        if not self.custom_id:
            prefix = 'GNG'
            last_guest = GuestEntry.objects.filter(custom_id__startswith=prefix).order_by('-custom_id').first()
            if last_guest and last_guest.custom_id:
                last_num = int(re.sub(r'^\D+', '', last_guest.custom_id))  # remove prefix letters
                new_num = last_num + 1
            else:
                new_num = 1
            self.custom_id = f'{prefix}{new_num:06d}'  # e.g. GNG/000001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.custom_id} - {self.full_name}"


    def get_status_color(self):
        """Returns Tabler badge color class based on status."""
        return {
            'Planted': 'success',
            'Planted Elsewhere': 'danger',
            'Relocated': 'primary',
            'Work in Progress': 'warning',
            'Select Status': 'secondary',
        }.get(self.status, 'secondary')

    def __str__(self):
        return self.full_name


class SocialMediaEntry(models.Model):
    SOCIAL_MEDIA_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'Tiktok'),
    ]

    guest = models.ForeignKey(
        'GuestEntry',
        on_delete=models.CASCADE,
        related_name='social_media_accounts'
    )
    platform = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)
    handle = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_platform_display()}: {self.handle}"



class FollowUpReport(models.Model):
    guest = models.ForeignKey(GuestEntry, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateField()
    note = models.TextField()
    service_sunday = models.BooleanField(default=False)
    service_midweek = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    # Assuming you want to track who created the report
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-report_date']
        unique_together = ['guest', 'report_date']  # Prevent duplicates
        
    def __str__(self):
        return f"{self.guest.full_name} - {self.report_date}"
