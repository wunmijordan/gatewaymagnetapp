# notifications/context_processors.py

from .models import Notification
from .models import UserSettings


def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        unread_count = notifications.count()
        return {
            "unread_notifications": notifications,
            "unread_count": unread_count
        }
    return {"unread_notifications": [], "unread_count": 0}



def user_settings(request):
    if request.user.is_authenticated:
        try:
            settings = request.user.settings
        except UserSettings.DoesNotExist:
            settings = None
        return {
            "settings": settings,
            "sound_choices": UserSettings.SOUND_CHOICES,
        }
    return {}
