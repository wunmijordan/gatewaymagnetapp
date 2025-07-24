from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import datetime
import pytz
from django.utils.timezone import localtime, now


DAY_QUOTES = {
    'Monday': "Start strong — the harvest is plenty!",
    'Tuesday': "God doesn't call the qualified — He qualifies the called.",
    'Wednesday': "It's the hump of the week. You're not alone in this mission.", 
    'Thursday': "It's Midweek Recharge: Reload your Artillery.",
    'Friday': "The weekend is here — prepare for His people.",
    'Saturday': "Pray. Plan. Prepare for the Sunday harvest.",
    'Sunday': "Today is the Lord’s day — Souls are waiting!",
}



from django.utils.timezone import localtime, now
import pytz

def post_login_redirect(request):
    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)
    today_str = now_in_wat.strftime('%Y-%m-%d')
    day_name = now_in_wat.strftime('%A')
    time_str = now_in_wat.strftime('%I:%M %p')

    seen_today = request.session.get('welcome_shown') == today_str

    if not seen_today:
        request.session['welcome_shown'] = today_str
        request.session.modified = True  # ✅ Tell Django the session has changed

        quote = DAY_QUOTES.get(day_name, "Stay faithful — your work in the Kingdom is never in vain.")

        return render(request, 'accounts/welcome_modal.html', {
            'day_name': day_name,
            'time_str': time_str,
            'quote': quote,
        })

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

