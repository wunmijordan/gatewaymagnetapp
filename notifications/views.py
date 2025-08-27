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


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserSettingsForm

@login_required
def user_settings(request):
    settings = request.user.settings

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # For GET, we don't need to return anything; modal is already in base.html
    return JsonResponse({"success": True})



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import UserSettings

@login_required
@require_POST
def update_user_settings(request):
    sound = request.POST.get("notification_sound", "chime1")
    vibration = request.POST.get("vibration_enabled") == "on"

    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    settings.notification_sound = sound
    settings.vibration_enabled = vibration
    settings.save()

    return JsonResponse({"status": "ok", "sound": sound, "vibration": vibration})
