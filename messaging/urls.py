from django.urls import path
from . import views

urlpatterns = [
  path('send/', views.send_bulk_message, name='send_bulk_message'),
  path('message/<int:guest_id>/', views.send_guest_message, name='send_guest_message'),
  path('ajax/get-guests/', views.get_guests_by_status, name='ajax_get_guests'),
]
