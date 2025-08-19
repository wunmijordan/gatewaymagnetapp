# accounts/management/commands/migrate_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as OldUser
from accounts.models import Profile

CustomUser = get_user_model()

class Command(BaseCommand):
  help = "Migrate old User + Profile into CustomUser"

  def handle(self, *args, **kwargs):
    for user in OldUser.objects.all():
      profile = getattr(user, "profile", None)
      full_name = profile.full_name if profile else f"{user.first_name} {user.last_name}"

      custom_user, created = CustomUser.objects.get_or_create(
        username=user.username,
        defaults={
          "email": user.email,
          "full_name": full_name,
          "phone_number": profile.phone_number if profile else "",
          "image": profile.image.name if profile and profile.image else None,
          "is_staff": user.is_staff,
          "is_superuser": user.is_superuser,
        }
      )

      if not created:
        self.stdout.write(self.style.WARNING(f"User {user.username} already migrated"))
      else:
        # preserve password
        custom_user.password = user.password
        custom_user.save()
        self.stdout.write(self.style.SUCCESS(f"Migrated {user.username}"))
