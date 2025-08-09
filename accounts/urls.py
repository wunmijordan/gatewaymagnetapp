# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('create-user/', views.create_user_view, name='create_user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
