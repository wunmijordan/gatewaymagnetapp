from django.contrib.auth import get_user_model
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from guests.models import GuestEntry
from accounts.utils import user_in_groups
from django.utils import timezone



User = get_user_model()

# Define staff groups globally
STAFF_GROUPS = ["Pastor", "Team Lead", "Admin"]


def guest_full_name(guest):
    """Return guest's full name with title if available."""
    if not guest:
        return "Unknown Guest"
    title = getattr(guest, "title", "")
    name = getattr(guest, "full_name", "Unnamed Guest")
    return f"{title} {name}".strip()


def user_full_name(user):
    """
    Return user's full name with title if available.
    Always prioritizes CustomUser.full_name before Django's get_full_name.
    """
    if not user:
        return "Unknown User"

    title = getattr(user, "title", "") or ""
    name = None

    # 🔑 Always prefer custom `full_name`
    if getattr(user, "full_name", None):
        name = user.full_name.strip()
    # Fallback: Django's AbstractUser get_full_name()
    elif hasattr(user, "get_full_name") and user.get_full_name().strip():
        name = user.get_full_name().strip()
    # Otherwise fallback to username
    elif getattr(user, "username", None):
        name = user.username
    else:
        name = "Unnamed User"

    return f"{title} {name}".strip() if title else name


def push_realtime_notification(notification):
    """
    Send a real-time notification to the user's WebSocket group.
    """
    channel_layer = get_channel_layer()
    group_name = f"user_{notification.user.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",  # must match consumer method
            "content": {
                "id": notification.id,
                "title": notification.title,
                "description": notification.description,
                "link": notification.link or "#",
                "is_urgent": notification.is_urgent,
                "is_success": notification.is_success,
            },
        },
    )


def notify_users(users, title, description, link="#", is_urgent=False, is_success=False):
    """
    Create in-app notifications for a set of users and push real-time updates.
    """
    for user in users:
        notif = Notification.objects.create(
            user=user,
            title=title,
            description=description,
            link=link,
            is_urgent=is_urgent,
            is_success=is_success,
        )
        push_realtime_notification(notif)



def get_user_role(user):
    """Return the role of a user as string for notification purposes."""
    if not user:
        return "Unknown"
    if user.is_superuser:
        return "Superuser"
    elif user_in_groups(user, STAFF_GROUPS):
        # Return the first matching group as role
        for group in STAFF_GROUPS:
            if user_in_groups(user, group):
                return group
    elif user_in_groups(user, "Message Manager"):
        return "Message Manager"
    elif user_in_groups(user, "Registrant"):
        return "Registrant"
    else:
        return "Team Member"
