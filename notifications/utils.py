from django.contrib.auth import get_user_model
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from guests.models import GuestEntry

User = get_user_model()


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


def get_superusers():
    return User.objects.filter(is_superuser=True)


def get_staff_excluding_superusers():
    return User.objects.filter(is_staff=True, is_superuser=False)


def get_regular_users():
    return User.objects.filter(is_staff=False, is_superuser=False)


def get_user_role(user):
    """Return the role of a user as string for notification purposes."""
    if not user:
        return "Unknown"
    if user.is_superuser:
        return "Superuser"
    elif user.is_staff:
        return "Admin"
    elif user.groups.filter(name="Message Manager").exists():
        return "Message Manager"
    elif user.groups.filter(name="Registrant").exists():
        return "Registrant"
    else:
        return "Team Member"
