from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Profile
from notifications.models import Notification
from guests.models import GuestEntry

User = get_user_model()


def get_superusers():
    return User.objects.filter(is_superuser=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)


@receiver(user_logged_in)
def notify_superuser_user_login(sender, request, user, **kwargs):
    if user.is_superuser:
        return  # skip superuser logins

    user_name = getattr(user.profile, 'full_name', user.username)
    guest_count = GuestEntry.objects.count()

    subject = f"[Login] {user_name} just logged in"
    message = f"{user_name} logged in.\nCurrent guest count: {guest_count}"

    # Email only in production
    if not settings.DEBUG:
        for su in get_superusers():
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [su.email])
            except Exception as e:
                print(f"Email not sent: {e}")

    # In-app notifications
    for su in get_superusers():
        Notification.objects.create(
            user=su,
            title="User Login",
            description=message,
            link=f"/accounts/users/{user.pk}/edit/",  # link to user profile
            is_urgent=True  # user logins are urgent
        )
