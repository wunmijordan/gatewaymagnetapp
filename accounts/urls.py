from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path("manage-groups/", views.manage_groups, name="manage_groups"),
    path("groups/delete/<int:group_id>/", views.delete_group, name="delete_group"),
    #path("page/", views.chat_page, name="chat_page"),
    path("chat/", views.chat_room, name="chat_room"),
    #path('api/messages/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    #path('api/messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    #path('api/guests/<int:guest_id>/', views.guest_detail_api, name='guest_detail_api'),
    #path('api/fetch-history/', views.fetch_history, name='fetch_history'),
    #path("chat/send/", views.send_chat_message, name="send_chat_message"),
    #path("chat/fetch/", views.fetch_chat_messages, name="fetch_chat_messages"),
]
