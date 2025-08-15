# notifications/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"



