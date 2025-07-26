from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

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

    picture = models.ImageField(
        upload_to='guest_pictures/',
        default='https://res.cloudinary.com/dahx6bbyr/image/upload/v1753468187/default_guest_memhgq.jpg',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=20, choices=TITLE_CHOICES, blank=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    phone_number = models.CharField(max_length=20, blank=True, null= True)
    email = models.EmailField(blank=True)
    date_of_birth = models.CharField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    home_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    date_of_visit = models.DateField(blank=True, null= True)
    purpose_of_visit = models.CharField(max_length=30, choices=PURPOSE_CHOICES, blank=True)
    channel_of_visit = models.CharField(max_length=30, choices=CHANNEL_CHOICES, blank=True)
    service_attended = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True)
    referrer_name = models.CharField(max_length=100, blank=True)
    referrer_phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Select Status')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_guests')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_guests')

    def get_status_color(self):
        """Returns Tabler badge color class based on status."""
        return {
            'Planted': 'success',
            'Planted Elsewhere': 'danger',
            'Relocated': 'primary',
            'Work in Progress': 'warning',
            'Select Status': 'secondary',
        }.get(self.status, 'primary')

    def __str__(self):
        return self.full_name


class FollowUpReport(models.Model):
    guest = models.ForeignKey(GuestEntry, on_delete=models.CASCADE, related_name='followup_reports')
    report_date = models.DateField()
    notes = models.TextField()
    attended_sunday = models.BooleanField(default=False)
    attended_midweek = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-report_date']
        unique_together = ['guest', 'report_date']  # Prevent duplicates
        
    def __str__(self):
        return f"{self.guest.full_name} - {self.report_date}"
