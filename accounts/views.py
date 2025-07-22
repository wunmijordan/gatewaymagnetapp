from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import datetime
import pytz
from django.utils.timezone import localtime, now

def post_login_redirect(request):
    """
    View shown right after login, checks if the user has seen the welcome popup today.
    """

    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)
    today_str = now_in_wat.strftime('%Y-%m-%d')
    seen_today = request.session.get('welcome_shown') == today_str

    if not seen_today:
        # Set session flag to prevent repeat today
        request.session['welcome_shown'] = today_str

        # Get day name and current time
        day_name = now_in_wat.strftime('%A')
        time_str = now_in_wat.strftime('%I:%M %p')  # e.g., "03:25 PM WAT"

        return render(request, 'accounts/welcome_modal.html', {
            'day_name': day_name,
            'time_str': time_str,
        })

    # If already seen, go straight to dashboard
    return redirect('dashboard')



def is_admin_or_superuser(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin_or_superuser)
def create_user_view(request):
    """
    Allows superusers and users in the 'Admin' group to create new users.
    """
    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or a success page

    return render(request, 'accounts/create_user.html', {
        'form': form
    })

