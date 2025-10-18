import pytz
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.utils.timezone import make_aware
from .models import Event
from .broadcast import broadcast_event

# Initialize scheduler
scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())


def schedule_event_notifications():
    """
    Schedule broadcast_event() for all active upcoming events.
    Automatically clears and refreshes jobs on every call.
    """
    print("🟡 [Scheduler] schedule_event_notifications() called")

    try:
        # Clear previous jobs to avoid duplicates
        scheduler.remove_all_jobs()

        events = Event.objects.filter(is_active=True, date__isnull=False, time__isnull=False)
        print(f"🟢 [Scheduler] Found {events.count()} events to schedule")

        now = timezone.now()

        for event in events:
            event_dt = make_aware(datetime.combine(event.date, event.time))

            # Skip past events
            if event_dt <= now:
                print(f"⏩ [Scheduler] Skipping past event: {event.name} ({event_dt})")
                continue

            # Broadcast a little early (e.g., 45 seconds before event)
            run_time = event_dt - timedelta(seconds=45)
            if run_time < now:
                run_time = now + timedelta(seconds=5)

            job_id = f"attendance_event_{event.id}"
            print(f"⏰ [Scheduler] Scheduling '{event.name}' at {run_time} (job id={job_id})")

            scheduler.add_job(
                broadcast_event,
                "date",
                run_date=run_time,
                args=[event],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=30,
            )

    except Exception as e:
        print(f"❌ [Scheduler] Error scheduling events: {e}")


def start():
    """
    Start scheduler safely in a background thread (so it works under ASGI).
    """
    print("🚀 [Scheduler] start() called")

    if getattr(scheduler, "_started", False):
        print("⚠️ [Scheduler] Already running")
        return

    def run_scheduler():
        try:
            scheduler.start()
            scheduler._started = True
            print("✅ [Scheduler] Started successfully")

            # Schedule events after short delay (so DB definitely ready)
            threading.Timer(2.0, schedule_event_notifications).start()
            print("✅ [Scheduler] Running with timezone:", scheduler.timezone)

        except Exception as e:
            print(f"❌ [Scheduler] Failed to start: {e}")

    # Run scheduler in a daemon thread
    threading.Thread(target=run_scheduler, daemon=True).start()
