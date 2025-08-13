from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm, UserEditForm, ProfileForm, UserForm
from django.contrib.auth.models import Group, User
from django.utils import timezone
from datetime import datetime
import pytz
from django.utils.timezone import localtime, now
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages


 

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 28)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')





DAY_QUOTES = {
    'Monday': "Start strong — the harvest is plenty!",
    'Tuesday': "God doesn't call the qualified — He qualifies the called.",
    'Wednesday': "It's the hump of the week. You're not alone in this mission.", 
    'Thursday': "It's Midweek Recharge: Reload your Artillery.",
    'Friday': "The weekend is here — prepare for His people.",
    'Saturday': "Pray. Plan. Prepare for the Sunday harvest.",
    'Sunday': "Today is the Lord’s day — Souls are waiting!",
}



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





User = get_user_model()
def is_superuser(user):
    return user.is_superuser

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    query = request.GET.get("q", "")
    users = User.objects.all().order_by("username")
    if query:
        users = users.filter(username__icontains=query)

    paginator = Paginator(users, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # If this is an HTMX request, return only the table body
    if request.htmx:
        return render(request, "accounts/partials/user_table.html", {"page_obj": page_obj})

    return render(request, "accounts/user_list.html", {"page_obj": page_obj})

@login_required
@user_passes_test(is_superuser)
def edit_user(request, pk,):
    user = User.objects.get(pk=pk)
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)  # email, is_active, etc.
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_list')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })

@login_required
@user_passes_test(is_superuser)
def delete_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')

    return render(request, 'accounts/confirm_user_delete.html', {'user': user_obj})