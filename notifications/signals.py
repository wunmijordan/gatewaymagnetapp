from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.urls import reverse
from django.apps import apps
from notifications.models import Notification

User = get_user_model()


# ---------- Helpers ----------
def get_user_full_name(user):
    """Return full_name if set, else username."""
    if not user:
        return "Unknown"
    return getattr(user, "full_name", None) or user.username or "Unknown"


def get_superusers():
    return User.objects.filter(is_superuser=True)


def notify_superusers(title, description, link, is_urgent=False, is_success=False, email_subject=None):
    """Helper to create DB notifications + send emails to superusers."""
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


# ---------- Lazy Guest model ----------
def get_guest_model():
    return apps.get_model("guests", "GuestEntry")


def get_guest_full_name(guest):
    return getattr(guest, "full_name", "Unknown")


# ---------- GuestEntry Signals ----------
@receiver(post_save, sender=get_guest_model())
def notify_superuser_guest_creation(sender, instance, created, **kwargs):
    if not created:
        return

    guest_name = get_guest_full_name(instance)
    creator_name = get_user_full_name(getattr(instance, "created_by", None))
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = get_guest_model().objects.count()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Created by: {creator_name}\n"
        f"Total Guests: {guest_count}"
    )

    link = reverse("guest_detail", args=[custom_id])  # adjust route name
    notify_superusers(
        title="Guest Created",
        description=description,
        link=link,
        is_success=True,
        email_subject=f"[Guest Created] {guest_name} ({custom_id})"
    )


@receiver(post_delete, sender=get_guest_model())
def notify_superuser_guest_deletion(sender, instance, **kwargs):
    guest_name = get_guest_full_name(instance)
    deleter_name = get_user_full_name(getattr(instance, "created_by", None))
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = get_guest_model().objects.count()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Deleted by: {deleter_name}\n"
        f"Total Guests: {guest_count}"
    )

    link = reverse("guest_list")
    notify_superusers(
        title="Guest Deleted",
        description=description,
        link=link,
        is_urgent=True,
        email_subject=f"[Guest Deleted] {guest_name} ({custom_id})"
    )


# ---------- User login signal ----------
@receiver(user_logged_in)
def notify_superuser_user_login(sender, request, user, **kwargs):
    if user.is_superuser:
        return

    user_name = get_user_full_name(user)
    guest_count = get_guest_model().objects.count()

    description = f"{user_name} logged in.\nCurrent guest count: {guest_count}"
    link = reverse("accounts:edit_user", args=[user.pk])

    notify_superusers(
        title="User Login",
        description=description,
        link=link,
        is_urgent=True,
        is_success=False,
        email_subject=f"[Login] {user_name} just logged in"
    )


# ---------- Optional: User Created/Deleted ----------
@receiver(post_save, sender=User)
def notify_superuser_user_creation(sender, instance, created, **kwargs):
    if not created:
        return
    creator = getattr(instance, "created_by", None)
    description = f"New user created: {get_user_full_name(instance)}\nCreated by: {get_user_full_name(creator)}"
    link = reverse("accounts:edit_user", args=[instance.pk])
    notify_superusers(
        title="User Created",
        description=description,
        link=link,
        is_success=True,
        email_subject=f"[User Created] {get_user_full_name(instance)}"
    )


@receiver(post_delete, sender=User)
def notify_superuser_user_deletion(sender, instance, **kwargs):
    description = f"User deleted: {get_user_full_name(instance)}"
    link = reverse("accounts:user_list")
    notify_superusers(
        title="User Deleted",
        description=description,
        link=link,
        is_urgent=True,
        email_subject=f"[User Deleted] {get_user_full_name(instance)}"
    )
