# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def mark_notification_read(request, pk):
    """Mark a single notification as read."""
    try:
        notif = Notification.objects.get(pk=pk, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({"status": "ok"})
    except Notification.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Notification not found"}, status=404)



@login_required
@csrf_exempt
def mark_all_read(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        request.user.notifications.filter(id__in=ids).update(is_read=True)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
def unread_notifications(request):
    """Return unread notifications for the logged-in user"""
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    data = {
        "unread_count": notifications.count(),
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "description": n.description,
                "link": n.link or "#",
                "is_urgent": n.is_urgent,
                "is_success": n.is_success,
            }
            for n in notifications
        ]
    }
    return JsonResponse(data)