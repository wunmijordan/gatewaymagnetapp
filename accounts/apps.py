from django.apps import AppConfig
import threading, time
from django.db import connections
from django.db.utils import OperationalError


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals
        from . import scheduler

        def safe_start_scheduler():
            """Wait until DB is ready before starting the scheduler."""
            for _ in range(10):  # retry up to ~10 seconds
                try:
                    connections["default"].cursor()
                    break
                except OperationalError:
                    print("⏳ [Scheduler] Waiting for DB to be ready...")
                    time.sleep(1)
            else:
                print("❌ [Scheduler] DB not ready. Scheduler start aborted.")
                return

            if not getattr(scheduler, "_started", False):
                scheduler.start()
                scheduler._started = True

        # Delay thread start slightly to avoid race with app initialization
        threading.Timer(1.0, safe_start_scheduler).start()
        # Import signals to ensure they are registered
        # This is necessary to connect the signals defined in accounts/signals.py
        # to the appropriate events in the Django lifecycle.
        # This line ensures that the signals are loaded when the app is ready.
        # If you have any signal handlers, they should be defined in accounts/signals.py
        # and will be automatically connected when the app is ready.
        # This is a common practice in Django to ensure that signal handlers are registered
        # when the application starts, allowing them to respond to events such as model saves,
        # deletions, or other actions.
        # Make sure to create the accounts/signals.py file and define your signal handlers there.
        # Example signal handler could be:
        # from django.db.models.signals import post_save
        # from django.dispatch import receiver
        # from .models import User
