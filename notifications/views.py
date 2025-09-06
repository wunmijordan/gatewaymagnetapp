# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification, UserSettings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notification

# Get unread notifications
@login_required
def unread_notifications(request):
    """Return all unread notifications for the logged-in user."""
    unread = request.user.notifications.filter(is_read=False).values(
        "id", "title", "description", "link", "created_at", "is_urgent", "is_success"
    )
    return JsonResponse(list(unread), safe=False)

# Mark a single notification as read
@login_required
@csrf_exempt
def mark_notification_read(request, pk):
    if request.method == "POST":
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return JsonResponse({"status": "ok"})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)

# Mark all notifications as read
@login_required
@csrf_exempt
def mark_all_read(request):
    if request.method == "POST":
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)




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

import json
from django.views.decorators.csrf import csrf_exempt  # not needed if CSRF token is sent

@login_required
@require_POST
def update_user_settings(request):
    try:
        data = json.loads(request.body)
    except:
        data = request.POST

    sound = data.get("notification_sound", "chime1")
    vibration = data.get("vibration_enabled", False)

    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    settings.notification_sound = sound
    settings.vibration_enabled = vibration
    settings.save()

    return JsonResponse({"status": "ok", "sound": sound, "vibration": vibration})

