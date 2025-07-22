# guests/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('entry/', views.guest_entry_view, name='guest_entry'),
    path('entry/<int:pk>/', views.guest_entry_view, name='edit_guest'),
    path('status/<int:pk>/', views.update_guest_status, name='update_guest_status'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('guest/<int:guest_id>/status/<str:status_key>/', views.update_status_view, name='update_status'),
    path('export/excel/', views.export_guests_excel, name='export_excel'),
    path('import/excel/', views.import_guests_excel, name='import_excel'),
    path('followup/<int:guest_id>/form/', views.get_followup_form, name='get_followup_form'),
    path('followup/<int:guest_id>/submit/', views.submit_followup_report, name='submit_followup_report'),
    path('followup/<int:report_id>/edit/', views.edit_followup_report, name='edit_followup_report'),
    path('followup/<int:report_id>/delete/', views.delete_followup_report, name='delete_followup_report'),
    path('guests/<int:guest_id>/followup/', views.followup_history_view, name='followup_history'),
    path('guests/export/pdf/', views.export_guests_pdf, name='export_guests_pdf'),
    path('guests/<int:guest_id>/followup/export/pdf/', views.export_followup_report_pdf, name='export_followup_report_pdf'),
]
