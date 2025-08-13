# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('create-user/', views.create_user_view, name='create_user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/edit/", views.edit_user, name="edit_user"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),
]
