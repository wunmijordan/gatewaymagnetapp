# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification, UserSettings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from .models import PushSubscription
from .utils import notify_users
from .models import UserSettings


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
    settings = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # For GET, we don't need to return anything; modal is already in base.html
    return JsonResponse({"success": True})


@login_required
@require_POST
def update_user_settings(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    try:
        data = json.loads(request.body)
    except:
        data = request.POST

    settings.notification_sound = data.get("notification_sound", settings.notification_sound)
    settings.vibration_enabled = data.get("vibration_enabled") in [True, "true", "on", "1"]
    settings.save()

    return JsonResponse({
        "status": "ok",
        "sound": settings.notification_sound,
        "vibration": settings.vibration_enabled
    })



@csrf_exempt
@login_required
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        PushSubscription.objects.update_or_create(
            user=request.user,
            defaults={"subscription_data": data}
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "invalid request"}, status=400)

@login_required
def test_push(request):
    sub = PushSubscription.objects.filter(user=request.user).first()
    if not sub:
        return JsonResponse({"error": "no subscription"}, status=400)

    send_push(
        sub.subscription_data,
        title="Hello!",
        body="This is a test push notification.",
        url="/"
    )
    return JsonResponse({"status": "sent"})

