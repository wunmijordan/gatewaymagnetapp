from django.core.management.base import BaseCommand
from accounts.scheduler import start

class Command(BaseCommand):
    help = "Start the background scheduler for event notifications."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting scheduler..."))
        try:
            start()
            self.stdout.write(self.style.SUCCESS("✅ Scheduler started successfully."))
        except RuntimeError as e:
            if "already running" in str(e).lower():
                self.stdout.write(self.style.WARNING("⚠️ Scheduler already running, skipping new start."))
            else:
                self.stderr.write(self.style.ERROR(f"❌ Scheduler failed: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Scheduler error: {e}"))
