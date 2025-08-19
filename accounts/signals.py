"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.urls import reverse
from guests.models import GuestEntry
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# ---------- Helpers ----------
def get_user_full_name(user):
#    Return full_name if set, else username.
    if not user:
        return "Unknown"
    return getattr(user, "full_name", None) or user.username or "Unknown"

def get_superusers():
    return User.objects.filter(is_superuser=True)

def notify_superusers(title, description, link, is_urgent=False, is_success=False, email_subject=None):
#    Helper to create DB notifications + send emails.
    for su in get_superusers():
        Notification.objects.create(
            user=su,
            title=title,
            description=description,
            link=link,
            is_urgent=is_urgent,
            is_success=is_success,
        )

        if not settings.DEBUG and su.email:
            try:
                send_mail(
                    subject=email_subject or title,
                    message=description,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[su.email],
                )
            except Exception as e:
                print(f"Email not sent to {su.email}: {e}")

# ---------- User login signal ----------
@receiver(user_logged_in)
def notify_superuser_user_login(sender, request, user, **kwargs):
    if user.is_superuser:
        return

    user_name = get_user_full_name(user)
    guest_count = GuestEntry.objects.count()

    description = f"{user_name} logged in.\nCurrent guest count: {guest_count}"
    link = reverse("accounts:user_edit", args=[user.pk])  # adjust route name

    notify_superusers(
        title="User Login",
        description=description,
        link=link,
        is_urgent=True,
        email_subject=f"[Login] {user_name} just logged in"
    )

# ---------- Example: User created ----------
@receiver(post_save, sender=User)
def notify_superuser_user_creation(sender, instance, created, **kwargs):
    if not created:
        return
    creator = getattr(instance, "created_by", None)
    creator_name = get_user_full_name(creator)
    user_name = get_user_full_name(instance)

    description = f"New user created: {user_name}\nCreated by: {creator_name}"
    link = reverse("accounts:user_edit", args=[instance.pk])  # adjust route

    notify_superusers(
        title="User Created",
        description=description,
        link=link,
        is_success=True,
        email_subject=f"[User Created] {user_name}"
    )

# ---------- Example: User deleted ----------
@receiver(post_delete, sender=User)
def notify_superuser_user_deletion(sender, instance, **kwargs):
    user_name = get_user_full_name(instance)

    description = f"User deleted: {user_name}"
    link = reverse("accounts:user_list")  # adjust route

    notify_superusers(
        title="User Deleted",
        description=description,
        link=link,
        is_urgent=True,
        email_subject=f"[User Deleted] {user_name}"
    )
"""