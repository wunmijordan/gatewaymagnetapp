from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.urls import reverse_lazy, reverse
from django.utils.timezone import localtime, now
import pytz
from django.contrib.auth import get_user_model
from guests.models import GuestEntry
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
import calendar
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupForm






User = get_user_model()

DAY_QUOTES = {
    'Monday': "Start strong — the harvest is plenty!",
    'Tuesday': "God doesn't call the qualified — He qualifies the called.",
    'Wednesday': "It's the hump of the week. You're not alone in this mission.", 
    'Thursday': "It's Midweek Recharge: Reload your Artillery.",
    'Friday': "The weekend is here — prepare for His people.",
    'Saturday': "Pray. Plan. Prepare for the Sunday harvest.",
    'Sunday': "Today is the Lord’s day — Souls are waiting!",
}


class CustomLoginForm(AuthenticationForm):
    pass


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
        return reverse_lazy('post_login_redirect')


def post_login_redirect(request):
    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)
    today_str = now_in_wat.strftime('%Y-%m-%d')
    day_name = now_in_wat.strftime('%A')
    time_str = now_in_wat.strftime('%I:%M %p')

    if request.session.get('welcome_shown') != today_str:
        request.session['welcome_shown'] = today_str
        request.session.modified = True
        quote = DAY_QUOTES.get(day_name, "Stay faithful — your work in the Kingdom is never in vain.")

        # Everyone with elevated roles goes to admin_dashboard
        if (
            request.user.is_superuser or
            request.user.is_staff or
            request.user.groups.filter(name__in=["Message Manager", "Registrant"]).exists()
        ):
            dashboard_url = reverse('accounts:admin_dashboard')
            dashboard_label = "Proceed to Dashboard"
        else:
            dashboard_url = reverse('dashboard')
            dashboard_label = "Proceed to Dashboard"

        return render(request, 'accounts/welcome_modal.html', {
            'day_name': day_name,
            'time_str': time_str,
            'quote': quote,
            'dashboard_url': dashboard_url,
            'dashboard_label': dashboard_label,
        })

    # If welcome already shown
    if (
        request.user.is_superuser or
        request.user.is_staff or
        request.user.groups.filter(name__in=["Message Manager", "Registrant"]).exists()
    ):
        return redirect('accounts:admin_dashboard')
    else:
        return redirect('dashboard')



User = get_user_model()

def is_admin_or_superuser(user):
    return user.is_staff or user.is_superuser or user.groups.filter(name__in=["Message Manager", "Registrant"]).exists()


@login_required
@user_passes_test(is_admin_or_superuser)
def admin_dashboard(request):
    """
    Admin/Superuser dashboard with all user stats and charts.
    Superuser sees all guests and users.
    Admin sees all guests but not superuser accounts.
    """
    user = request.user
    current_year = datetime.now().year

    # Role-based queryset
    if user.is_superuser:
        # Full access
        queryset = GuestEntry.objects.all()
        users = User.objects.all().order_by('full_name')

    elif user.is_staff:
        # Admin: all guests, but exclude superusers from user stats
        queryset = GuestEntry.objects.all()
        users = User.objects.filter(is_superuser=False).order_by('full_name')

    else:
        user.groups.filter(name__in=["Message Manager", "Registrant"]).exists()
        # Message Manager & Registrant: only guests, no users
        queryset = GuestEntry.objects.all()
        users = None

    # Available years
    available_years = queryset.dates('date_of_visit', 'year')
    available_years = [d.year for d in available_years]

    # === Yearly guest summary (monthly breakdown) ===
    year = request.GET.get('year', current_year)
    try:
        year = int(year)
    except (TypeError, ValueError):
        year = current_year

    guests_this_year = queryset.filter(date_of_visit__year=year)
    total_count = guests_this_year.count()

    month_counts_qs = (
        guests_this_year.annotate(month=ExtractMonth('date_of_visit'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    month_counts = {m: 0 for m in range(1, 13)}
    for entry in month_counts_qs:
        month_counts[entry['month']] = entry['count']

    max_count = max(month_counts.values()) if month_counts else 0
    min_count = min(month_counts.values()) if month_counts else 0
    avg_count = sum(month_counts.values()) // 12 if month_counts else 0
    max_months = [calendar.month_name[m] for m, c in month_counts.items() if c == max_count]
    min_months = [calendar.month_name[m] for m, c in month_counts.items() if c == min_count]
    max_month = max_months[0] if max_months else "N/A"
    min_month = min_months[0] if min_months else "N/A"
    

    def percent(count):
        return round((count / max_count) * 100, 1) if max_count else 0

    summary_data = {
        'max_month': max_month,
        'max_count': max_count,
        'max_percent': percent(max_count),
        'min_month': min_month,
        'min_count': min_count,
        'min_percent': percent(min_count),
        'avg_count': avg_count,
        'avg_percent': percent(avg_count),
        'total_count': total_count,
    }

    # === Services attended data ===
    service_qs = queryset.values('service_attended').annotate(count=Count('id')).order_by('-count')
    service_labels = [s['service_attended'] or "Not Specified" for s in service_qs]
    service_counts = [s['count'] for s in service_qs]

    # === Channel breakdown data ===
    channel_qs = queryset.values('channel_of_visit').annotate(count=Count('id')).order_by('-count')
    total_channels = sum(c['count'] for c in channel_qs)
    channel_progress = [
        {
            'label': c['channel_of_visit'] or "Unknown",
            'count': c['count'],
            'percent': round((c['count'] / total_channels) * 100, 2) if total_channels else 0
        }
        for c in channel_qs
    ]

    # === Purpose stats ===
    total_purposes = queryset.count()
    home_church_count = queryset.filter(purpose_of_visit__iexact="Home Church").count()
    home_church_percentage = round((home_church_count / total_purposes) * 100, 1) if total_purposes else 0

    occasional_visit_count = queryset.filter(purpose_of_visit__iexact="Occasional Visit").count()
    occasional_visit_percentage = round((occasional_visit_count / total_purposes) * 100, 1) if total_purposes else 0

    one_time_visit_count = queryset.filter(purpose_of_visit__iexact="One-Time Visit").count()
    one_time_visit_percentage = round((one_time_visit_count / total_purposes) * 100, 1) if total_purposes else 0

    special_programme_count = queryset.filter(purpose_of_visit__iexact="Special Programme").count()
    special_programme_percentage = round((special_programme_count / total_purposes) * 100, 1) if total_purposes else 0

    # === Most attended service card ===
    if service_qs:
        most_attended_service = service_qs[0]['service_attended'] or "Not Specified"
        most_attended_count = service_qs[0]['count']
        total_services = sum(s['count'] for s in service_qs)
        attendance_rate = round((most_attended_count / total_services) * 100, 1) if total_services else 0
    else:
        most_attended_service = "No Data"
        most_attended_count = 0
        attendance_rate = 0

    # === Status stats ===
    status_qs = queryset.values('status').annotate(count=Count('id'))
    status_labels = [s['status'] or "Unknown" for s in status_qs]
    status_counts = [s['count'] for s in status_qs]

    # === Totals & statuses ===
    planted_count = queryset.filter(status="Planted").count()
    planted_elsewhere_count = queryset.filter(status="Planted Elsewhere").count()
    relocated_count = queryset.filter(status="Relocated").count()
    work_in_progress_count = queryset.filter(status="Work in Progress").count()

    # === Global total guests and monthly increase ===
    today = now().date()
    first_day_this_month = today.replace(day=1)
    last_month_end = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_month_end.replace(day=1)

    current_month_count = queryset.filter(date_of_visit__gte=first_day_this_month,
                                          date_of_visit__lte=today).count()
    last_month_count = queryset.filter(date_of_visit__gte=first_day_last_month,
                                       date_of_visit__lte=last_month_end).count()

    if last_month_count == 0:
        percent_change = 100 if current_month_count > 0 else 0
        increase_rate = percent_change
    else:
        difference = current_month_count - last_month_count
        increase_rate = round((difference / last_month_count) * 100, 1)
        percent_change = increase_rate

    # === Logged-in user's total guest entries & growth ===
    user_total_guest_entries = queryset.filter(assigned_to=user).count()
    user_current_month_count = queryset.filter(assigned_to=user,
                                               date_of_visit__gte=first_day_this_month,
                                               date_of_visit__lte=today).count()
    user_last_month_count = queryset.filter(assigned_to=user,
                                            date_of_visit__gte=first_day_last_month,
                                            date_of_visit__lte=last_month_end).count()

    if user_last_month_count == 0:
        user_diff_percent = 100 if user_current_month_count > 0 else 0
        user_diff_positive = True
    else:
        diff = ((user_current_month_count - user_last_month_count) / user_last_month_count) * 100
        user_diff_percent = round(abs(diff), 1)
        user_diff_positive = diff >= 0

    # === Planted guests growth for logged-in user ===
    user_planted_total = queryset.filter(assigned_to=user, status="Planted").count()
    planted_growth_rate = round((user_planted_total / user_total_guest_entries) * 100, 1) \
                          if user_total_guest_entries else 0

    user_planted_current_month = queryset.filter(assigned_to=user, status="Planted",
                                                 date_of_visit__gte=first_day_this_month,
                                                 date_of_visit__lte=today).count()
    user_planted_last_month = queryset.filter(assigned_to=user, status="Planted",
                                              date_of_visit__gte=first_day_last_month,
                                              date_of_visit__lte=last_month_end).count()
    if user_planted_last_month == 0:
        planted_growth_change = 100 if user_planted_current_month > 0 else 0
    else:
        diff = ((user_planted_current_month - user_planted_last_month) / user_planted_last_month) * 100
        planted_growth_change = round(diff, 1)

    context = {
        'show_filters': False,
        'available_years': available_years,
        'current_year': current_year,
        'summary_data': summary_data,
        'service_labels': service_labels,
        'service_counts': service_counts,
        'status_labels': status_labels,
        'status_counts': status_counts,
        'channel_progress': channel_progress,
        'planted_count': planted_count,
        'planted_elsewhere_count': planted_elsewhere_count,
        'relocated_count': relocated_count,
        'work_in_progress_count': work_in_progress_count,
        'total_guests': queryset.count(),
        'increase_rate': increase_rate,
        'percent_change': percent_change,
        'user_total_guest_entries': user_total_guest_entries,
        'user_guest_entry_diff_percent': user_diff_percent,
        'user_guest_entry_diff_positive': user_diff_positive,
        'user_planted_total': user_planted_total,
        'planted_growth_rate': planted_growth_rate,
        'planted_growth_change': planted_growth_change,
        'most_attended_service': most_attended_service,
        'most_attended_count': most_attended_count,
        'attendance_rate': attendance_rate,
        'home_church_count': home_church_count,
        'home_church_percentage': home_church_percentage,
        'occasional_visit_count': occasional_visit_count,
        'occasional_visit_percentage': occasional_visit_percentage,
        'one_time_visit_count': one_time_visit_count,
        'one_time_visit_percentage': one_time_visit_percentage,
        'special_programme_count': special_programme_count,
        'special_programme_percentage': special_programme_percentage,
        'users': users,
        'guests': queryset,
        'page_title': "Admin Dashboard",
    }

    return render(request, "accounts/admin_dashboard.html", context)








from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import SetPasswordForm

from .models import CustomUser

# Utility: check if user is superuser
def is_superuser_check(user):
    return user.is_superuser


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import CustomUser

@login_required
def user_list(request):
    """
    Display users for admin dashboard with search and pagination.
    Superusers see all users. Admin group sees non-superusers only.
    """
    search_query = request.GET.get('q', '')


    # Determine accessible users
    if request.user.is_superuser:
        users = CustomUser.objects.all()
    elif request.user.groups.filter(name="Admin").exists():
        users = CustomUser.objects.filter(is_superuser=False)
    else:
        messages.error(request, "You do not have permission to view users.")
        return redirect('accounts:admin_dashboard')

    # Apply search filter
    if search_query:
        users = users.filter(
            Q(full_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Pagination
    view_type = request.GET.get('view', 'cards')
    per_page = 50 if view_type == 'list' else 12
    paginator = Paginator(users, per_page)  # <-- paginate filtered users
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'accounts/user_list.html', {
        'users': page_obj.object_list,
        'page_obj': page_obj,
        'view_type': view_type,
        'search_query': search_query,
        'page_title': 'Team'
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@login_required
def create_user(request):
    """
    Create new users. Admin group cannot create superusers.
    """
    # Only superusers or Admin group can access
    if not request.user.is_superuser and not request.user.groups.filter(name="Admin").exists():
        messages.error(request, "You do not have permission to create users.")
        return redirect('accounts:user_list')

    if request.method == "POST":
        form = CustomUserCreationForm(
            request.POST, 
            request.FILES, 
            current_user=request.user
        )

        # Admins cannot create superusers
        if not request.user.is_superuser:
            form.instance.is_superuser = False

        if form.is_valid():
            user = form.save()

            messages.success(request, f"User {user.full_name} created successfully!")

            # Button routing
            if 'save_return' in request.POST:
                return redirect('accounts:user_list')
            elif 'save_add_another' in request.POST:
                return redirect('accounts:create_user')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm(current_user=request.user)


    return render(request, 'accounts/user_form.html', {
        'form': form,
        'edit_mode': False,
        'page_title': 'Team',
    })



@login_required
def edit_user(request, user_id):
    """
    Edit user profile. Admins cannot edit superusers.
    """
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    # Admins cannot edit superusers
    if not request.user.is_superuser and user_obj.is_superuser:
        messages.error(request, "You cannot edit a superuser.")
        return redirect('accounts:user_list')

    # Only superusers or Admin group can access
    if not request.user.is_superuser and not request.user.groups.filter(name="Admin").exists():
        messages.error(request, "You do not have permission to edit users.")
        return redirect('accounts:user_list')

    form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=user_obj, current_user=request.user, edit_mode=True)
    password_form = SetPasswordForm(user_obj)

    if request.method == "POST":
        # Delete User
        if 'delete_user' in request.POST:
            if user_obj.is_superuser:
                messages.error(request, "Cannot delete a superuser.")
            else:
                user_obj.delete()
                messages.success(request, f"User {user_obj.full_name} deleted successfully.")
            return redirect('accounts:user_list')

        # Deactivate/Reactivate User
        elif 'deactivate_user' in request.POST:
            if user_obj.is_superuser:
                messages.error(request, "Cannot deactivate a superuser.")
            else:
                user_obj.is_active = not user_obj.is_active
                user_obj.save()
                status = "activated" if user_obj.is_active else "deactivated"
                messages.success(request, f"User {user_obj.full_name} {status} successfully.")
            return redirect('accounts:user_list')

        # Change Password
        elif 'change_password' in request.POST:
            password_form = SetPasswordForm(user_obj, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, f"Password updated for {user_obj.full_name}.")
                return redirect('accounts:user_list')
            else:
                messages.error(request, "Please correct the password errors.")

        # Edit user/profile
        else:
            if form.is_valid():
                user_obj = form.save()

                messages.success(request, f"User {user_obj.full_name} updated successfully!")

                # Button routing
                if 'save_return' in request.POST:
                    return redirect('accounts:user_list')
                elif 'save_add_another' in request.POST:
                    return redirect('accounts:create_user')
            else:
                messages.error(request, "Please correct the errors below.")


    return render(request, 'accounts/user_form.html', {
        'form': form,
        'edit_mode': True,
        'user_obj': user_obj,
        'password_form': password_form,
        'page_title': 'Team',
    })


@login_required
def manage_groups(request):
    groups = Group.objects.all().order_by("name")
    form = GroupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect("accounts:manage_groups")
        else:
            messages.error(request, "Error creating group. Please try again.")

    return render(request, "accounts/manage_groups.html", {
        "groups": groups,
        "form": form,
    })








