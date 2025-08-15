from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from notifications.models import Notification
from guests.models import GuestEntry
from accounts.models import Profile

User = get_user_model()


# Helpers
def get_user_full_name(user):
  if not user:
    return "Unknown"
  profile = getattr(user, 'profile', None)
  if profile and profile.full_name:
    return profile.full_name
  full_name = f"{user.first_name} {user.last_name}".strip()
  return full_name if full_name else getattr(user, 'username', 'Unknown')


def get_guest_full_name(guest):
  return getattr(guest, 'full_name', 'Unknown')


def get_superusers():
  return User.objects.filter(is_superuser=True)


# Guest creation
@receiver(post_save, sender=GuestEntry)
def notify_superuser_guest_creation(sender, instance, created, **kwargs):
  if not created:
    return

  guest_name = get_guest_full_name(instance)
  guest_owner_name = get_user_full_name(instance.created_by)
  custom_id = getattr(instance, 'custom_id', 'N/A')
  guest_count = GuestEntry.objects.count()

  subject = f"[Guest Created] {guest_name} ({custom_id})"
  message = (
    f"{guest_name} ({custom_id})\n"
    f"Created by: {guest_owner_name}\n"
    f"Total Guests: {guest_count}"
  )

  if not settings.DEBUG:
    for su in get_superusers():
      try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [su.email])
      except Exception as e:
        print(f"Email not sent: {e}")

  for su in get_superusers():
    Notification.objects.create(
      user=su,
      title="Guest Created",
      description=message,
      link=f"/guest/{custom_id}/",
      is_urgent=False,
      is_success=True
    )


# Guest deletion
@receiver(post_delete, sender=GuestEntry)
def notify_superuser_guest_deletion(sender, instance, **kwargs):
  guest_name = get_guest_full_name(instance)
  deleting_user_name = get_user_full_name(instance.created_by)
  custom_id = getattr(instance, 'custom_id', 'N/A')
  guest_count = GuestEntry.objects.count()

  subject = f"[Guest Deleted] {guest_name} ({custom_id})"
  message = (
    f"{guest_name} ({custom_id})\n"
    f"Deleted by: {deleting_user_name}\n"
    f"Total Guests: {guest_count}"
  )

  if not settings.DEBUG:
    for su in get_superusers():
      try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [su.email])
      except Exception as e:
        print(f"Email not sent: {e}")

  for su in get_superusers():
    Notification.objects.create(
      user=su,
      title="Guest Deleted",
      description=message,
      link="/guests/",
      is_urgent=True,
      is_success=False
    )


# User login
@receiver(user_logged_in)
def notify_superuser_user_login(sender, request, user, **kwargs):
  if user.is_superuser:
    return

  user_name = getattr(user.profile, 'full_name', user.username)
  guest_count = GuestEntry.objects.count()

  subject = f"[Login] {user_name} just logged in"
  message = f"{user_name} logged in.\nCurrent guest count: {guest_count}"

  if not settings.DEBUG:
    for su in get_superusers():
      try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [su.email])
      except Exception as e:
        print(f"Email not sent: {e}")

  for su in get_superusers():
    Notification.objects.create(
      user=su,
      title="User Login",
      description=message,
      link=f"/accounts/users/{user.pk}/edit/",
      is_urgent=True,
      is_success=False
    )


# Ensure Profile exists for each User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
  else:
    try:
      instance.profile.save()
    except Profile.DoesNotExist:
      Profile.objects.create(user=instance)
