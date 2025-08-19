# notifications/urls.py
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("mark-read/<int:pk>/", views.mark_notification_read, name="mark_read"),
    path("mark-read-all/", views.mark_all_read, name="mark_read_all")
]
