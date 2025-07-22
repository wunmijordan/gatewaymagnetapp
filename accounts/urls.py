# accounts/urls.py
from django.urls import path
from .views import create_user_view
from django.contrib.auth import views as auth_views
from accounts.views import post_login_redirect

urlpatterns = [
    path('create-user/', create_user_view, name='create_user'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('post-login/', post_login_redirect, name='post_login_redirect'),
]
