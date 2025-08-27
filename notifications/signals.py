from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserSettings
from guests.models import GuestEntry
from django.urls import reverse
from notifications.middleware import get_current_user
from notifications.utils import (
    notify_users,
    get_superusers,
    get_staff_excluding_superusers,
    guest_full_name,
    user_full_name,
    get_user_role,
)

User = get_user_model()


# -----------------------------
# Guest Signals
# -----------------------------
@receiver(post_save, sender=GuestEntry)
def notify_guest_creation(sender, instance, created, **kwargs):
    if not created:
        return

    registrant = get_current_user()  # use currently logged-in user

    guest_name = guest_full_name(instance)
    creator_name = user_full_name(registrant)
    creator_role = get_user_role(registrant)
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = GuestEntry.objects.count()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Registered by: {creator_name}.\n"
        f"New Guests Count: {guest_count}"
    )
    link = reverse("guest_list")

    notify_users(get_superusers(), "Guest Created", description, link, is_success=True)
    notify_users(get_staff_excluding_superusers(), "Guest Created", description, link, is_success=True)


@receiver(post_delete, sender=GuestEntry)
def notify_guest_deletion(sender, instance, **kwargs):
    deleter = get_current_user()

    guest_name = guest_full_name(instance)
    deleter_name = user_full_name(deleter)
    deleter_role = get_user_role(deleter)
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = GuestEntry.objects.count()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Deleted by: {deleter_name} ({deleter_role})\n"
        f"New Guests Count: {guest_count}"
    )
    link = reverse("guest_list")

    notify_users(get_superusers(), "Guest Deleted", description, link, is_urgent=True)
    notify_users(get_staff_excluding_superusers(), "Guest Deleted", description, link, is_urgent=True)


@receiver(post_save, sender=GuestEntry)
def notify_guest_assignment(sender, instance, created, **kwargs):
    if created:
        return
    if instance.assigned_to:
        guest_name = guest_full_name(instance)
        description = f"You have been assigned guest: {guest_name} ({instance.custom_id})."
        link = reverse("guest_list")

        notify_users([instance.assigned_to], "Guest Assigned", description, link, is_success=True)
        notify_users(get_staff_excluding_superusers(), "Guest Assigned", description, link, is_success=True)


# -----------------------------
# User Signals
# -----------------------------
@receiver(post_save, sender=User)
def notify_user_creation(sender, instance, created, **kwargs):
    if not created:
        return
    description = f"New user created: {user_full_name(instance)}."
    link = reverse("accounts:edit_user", args=[instance.pk])

    notify_users(get_superusers(), "User Created", description, link, is_success=True)
    notify_users(get_staff_excluding_superusers(), "User Created", description, link, is_success=True)


@receiver(post_delete, sender=User)
def notify_user_deletion(sender, instance, **kwargs):
    description = f"User deleted: {user_full_name(instance)}."
    link = reverse("accounts:user_list")

    notify_users(get_superusers(), "User Deleted", description, link, is_urgent=True)
    notify_users(get_staff_excluding_superusers(), "User Deleted", description, link, is_urgent=True)


@receiver(user_logged_in)
def notify_user_login(sender, request, user, **kwargs):
    user_name = user_full_name(user)
    guest_count = GuestEntry.objects.count()

    description = f"{user_name} logged in."
    link = reverse("accounts:edit_user", args=[user.pk])

    notify_users(get_superusers(), "User Login", description, link, is_urgent=True)
    notify_users(get_staff_excluding_superusers(), "User Login", description, link, is_urgent=True)


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
