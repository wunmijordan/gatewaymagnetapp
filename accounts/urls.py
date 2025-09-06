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
    path("page/", views.chat_page, name="chat_page"),
    path("chat/send/", views.send_chat_message, name="send_chat_message"),
    path("chat/fetch/", views.fetch_chat_messages, name="fetch_chat_messages"),
]
