# broadcast.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import AttendanceRecord

broadcasted_events = set()

def broadcast_event(event):
    """Broadcast event start trigger once per event id."""
    if event.id in broadcasted_events:
        return
    broadcasted_events.add(event.id)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "attendance",
        {
            "type": "send_event",
            "data": {
                "id": event.id,
                "name": event.name,
                "date": str(event.date),
                "time": str(event.time),
            },
        },
    )

def broadcast_attendance_summary():
    """Broadcast updated attendance summary for all connected clients."""
    channel_layer = get_channel_layer()
    records = AttendanceRecord.objects.select_related("event", "user").order_by("-date")[:30]
    async_to_sync(channel_layer.group_send)(
        "attendance",
        {
            "type": "send_summary",
            "data": {
                "records": [
                    {
                        "date": r.date.isoformat(),
                        "event": r.event.name,
                        "user": f"{r.user.title or ''} {r.user.full_name}".strip(),
                        "status": r.status,
                        "remarks": r.remarks or "",
                    }
                    for r in records
                ]
            },
        },
    )
