import pytz
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Event
from .consumers import broadcast_event

scheduler = BackgroundScheduler(timezone=pytz.UTC)

def schedule_event_notifications():
    """
    Schedule broadcast_event() for all active events with a date and time.
    """
    events = Event.objects.filter(is_active=True, date__isnull=False, time__isnull=False)

    for event in events:
        # Convert event datetime to aware datetime in UTC
        from django.utils.timezone import make_aware
        event_dt = make_aware(datetime.combine(event.date, event.time))

        # Skip past events
        if event_dt <= datetime.now(tz=event_dt.tzinfo):
            continue

        # Schedule the broadcast
        scheduler.add_job(
            broadcast_event,
            'date',
            run_date=event_dt,
            args=[event],
            id=f"attendance_event_{event.id}",
            replace_existing=True
        )

def start():
    scheduler.start()
    schedule_event_notifications()
