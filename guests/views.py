from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import GuestEntry, FollowUpReport
from .forms import GuestEntryForm, FollowUpReportForm
import csv
import io
from django.utils.dateparse import parse_date
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.http import urlencode
import openpyxl
from openpyxl.utils import get_column_letter
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import localtime, now, localdate
import pytz
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Count, Max, F
from django.template.loader import get_template
import weasyprint
#from .utils import get_week_start_end
from guests.models import GuestEntry
from django.utils.dateparse import parse_date
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
import calendar
import base64
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import os
from django.db import IntegrityError




User = get_user_model()

#def is_admin_group(user):
#    return user.is_authenticated and user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(lambda u: is_admin_group)
def reassign_guest(request, guest_id):
    guest = get_object_or_404(GuestEntry, pk=guest_id)

    if request.method == "POST":
        assigned_to_id = request.POST.get("assigned_to")
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(pk=assigned_to_id)
                guest.assigned_to = assigned_user
                guest.save()
                messages.success(request, f"{guest.full_name} reassigned to {assigned_user.get_full_name() or assigned_user.username}.")
            except User.DoesNotExist:
                messages.error(request, "Selected user does not exist.")
        else:
            guest.assigned_to = None
            guest.save()
            messages.info(request, f"{guest.full_name} is now unassigned.")

    return redirect('guest_list')



@login_required
def dashboard_view(request):
    """Main dashboard view with server-rendered stats for cards and charts."""
    user = request.user
    current_year = datetime.now().year
    guest_entries = GuestEntry.objects.all()  # all guest entries for available years filter

    # Queryset for filtered data cards, charts (role based)
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        queryset = GuestEntry.objects.all()
    else:
        queryset = GuestEntry.objects.filter(created_by=user)

    available_years = guest_entries.dates('date_of_visit', 'year')
    available_years = [d.year for d in available_years]

    # Pre-fill for current year summary
    request.GET = request.GET.copy()
    request.GET['year'] = str(current_year)
    summary_json = guest_entry_summary(request)
    summary_data = summary_json.content.decode()

    # Services attended (used for most attended card & chart)
    service_qs = GuestEntry.objects.values('service_attended').annotate(count=Count('id')).order_by('-count')
    service_labels = [s['service_attended'] or "Not Specified" for s in service_qs]
    service_counts = [s['count'] for s in service_qs]

    # Home Church stats
    total_purposes = GuestEntry.objects.count()
    home_church_count = GuestEntry.objects.filter(purpose_of_visit__iexact="Home Church").count()
    home_church_percentage = round((home_church_count / total_purposes) * 100, 1) if total_purposes else 0

    # Occasional Visit stats
    occasional_visit_count = GuestEntry.objects.filter(purpose_of_visit__iexact="Occasional Visit").count()
    occasional_visit_percentage = round((occasional_visit_count / total_purposes) * 100, 1) if total_purposes else 0

    # One-Time Visit stats
    one_time_visit_count = GuestEntry.objects.filter(purpose_of_visit__iexact="One-Time Visit").count()
    one_time_visit_percentage = round((one_time_visit_count / total_purposes) * 100, 1) if total_purposes else 0

    # Special Programme stats
    special_programme_count = GuestEntry.objects.filter(purpose_of_visit__iexact="Special Programme").count()
    special_programme_percentage = round((special_programme_count / total_purposes) * 100, 1) if total_purposes else 0

    # Most attended service card data
    if service_qs:
        most_attended_service = service_qs[0]['service_attended'] or "Not Specified"
        most_attended_count = service_qs[0]['count']
        total_services = sum(s['count'] for s in service_qs)
        attendance_rate = round((most_attended_count / total_services) * 100, 1) if total_services else 0
    else:
        most_attended_service = "No Data"
        most_attended_count = 0
        attendance_rate = 0

    # Status data (for cards)
    status_qs = GuestEntry.objects.values('status').annotate(count=Count('id'))
    status_labels = [s['status'] or "Unknown" for s in status_qs]
    status_counts = [s['count'] for s in status_qs]

    # Channel of Visit
    channel_qs = GuestEntry.objects.values('channel_of_visit').annotate(count=Count('id')).order_by('-count')
    total_channels = sum(c['count'] for c in channel_qs)
    channel_progress = [
        {
            'label': c['channel_of_visit'] or "Unknown",
            'count': c['count'],
            'percent': round((c['count'] / total_channels) * 100, 2) if total_channels else 0
        }
        for c in channel_qs
    ]

    # Totals & stats for cards (role filtered)
    planted_count = GuestEntry.objects.filter(status="Planted").count()
    planted_elsewhere_count = GuestEntry.objects.filter(status="Planted Elsewhere").count()
    relocated_count = GuestEntry.objects.filter(status="Relocated").count()
    work_in_progress_count = GuestEntry.objects.filter(status="Work in Progress").count()

    # === Global total guests and monthly increase rate (all users) ===
    total_guests = GuestEntry.objects.count()

    today = now().date()
    first_day_this_month = today.replace(day=1)
    last_month_end = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_month_end.replace(day=1)

    current_month_count = GuestEntry.objects.filter(
        date_of_visit__gte=first_day_this_month,
        date_of_visit__lte=today
    ).count()

    last_month_count = GuestEntry.objects.filter(
        date_of_visit__gte=first_day_last_month,
        date_of_visit__lte=last_month_end
    ).count()

    if last_month_count == 0:
        if current_month_count > 0:
            increase_rate = 100
            percent_change = 100
        else:
            increase_rate = 0
            percent_change = 0
    else:
        difference = current_month_count - last_month_count
        increase_rate = round((difference / last_month_count) * 100, 1)
        percent_change = increase_rate

    # === Logged-in user's total guest entries and month difference ===
    user_total_guest_entries = GuestEntry.objects.filter(created_by=user).count()

    user_current_month_count = GuestEntry.objects.filter(
        created_by=user,
        date_of_visit__gte=first_day_this_month,
        date_of_visit__lte=today
    ).count()

    user_last_month_count = GuestEntry.objects.filter(
        created_by=user,
        date_of_visit__gte=first_day_last_month,
        date_of_visit__lte=last_month_end
    ).count()

    if user_last_month_count == 0:
        if user_current_month_count > 0:
            user_diff_percent = 100
            user_diff_positive = True
        else:
            user_diff_percent = 0
            user_diff_positive = True
    else:
        diff = ((user_current_month_count - user_last_month_count) / user_last_month_count) * 100
        user_diff_percent = round(abs(diff), 1)
        user_diff_positive = diff >= 0

    # === Planted guests growth rate for logged-in user ===
    user_planted_total = GuestEntry.objects.filter(created_by=user, status="Planted").count()
    planted_growth_rate = round((user_planted_total / user_total_guest_entries) * 100, 1) if user_total_guest_entries else 0

    user_planted_current_month = GuestEntry.objects.filter(
        created_by=user,
        status="Planted",
        date_of_visit__gte=first_day_this_month,
        date_of_visit__lte=today
    ).count()

    user_planted_last_month = GuestEntry.objects.filter(
        created_by=user,
        status="Planted",
        date_of_visit__gte=first_day_last_month,
        date_of_visit__lte=last_month_end
    ).count()

    if user_planted_last_month == 0:
        if user_planted_current_month > 0:
            planted_growth_change = 100
        else:
            planted_growth_change = 0
    else:
        diff = ((user_planted_current_month - user_planted_last_month) / user_planted_last_month) * 100
        planted_growth_change = round(diff, 1)

    # Load illustration image as base64
    #image_path = 'static/tabler/folders.png'
    #with open(image_path, 'rb') as img:
    #    image_data_uri = f"data:image/png;base64,{base64.b64encode(img.read()).decode()}"

    context = {
        'show_filters': False,
        'available_years': available_years,
        'current_year': current_year,
        'summary_data': json.loads(summary_data),
        "service_labels": service_labels,
        "service_counts": service_counts,
        "status_labels": status_labels,
        "status_counts": status_counts,
        "channel_progress": channel_progress,
        "planted_count": planted_count,
        "planted_elsewhere_count": planted_elsewhere_count,
        "relocated_count": relocated_count,
        "work_in_progress_count": work_in_progress_count,
        "total_guests": total_guests,               # Global total guests
        "increase_rate": increase_rate,             # Global monthly increase rate (%)
        "percent_change": percent_change,           # Same as increase_rate for display
        "user_total_guest_entries": user_total_guest_entries,     # User's total guest entries
        "user_guest_entry_diff_percent": user_diff_percent,       # User's month-over-month % difference (absolute)
        "user_guest_entry_diff_positive": user_diff_positive,     # Boolean if user diff is positive
        "user_planted_total": user_planted_total,
        "planted_growth_rate": planted_growth_rate,                # User planted % of total user guests
        "planted_growth_change": planted_growth_change,            # User planted MoM % change
        #"image_data_uri": image_data_uri,
        "most_attended_service": most_attended_service,
        "most_attended_count": most_attended_count,
        "attendance_rate": attendance_rate,
        "home_church_count": home_church_count,
        "home_church_percentage": home_church_percentage,
        "occasional_visit_count": occasional_visit_count,
        "occasional_visit_percentage": occasional_visit_percentage,
        "one_time_visit_count": one_time_visit_count,
        "one_time_visit_percentage": one_time_visit_percentage,
        "special_programme_count": special_programme_count,
        "special_programme_percentage": special_programme_percentage,
    }
    return render(request, "guests/dashboard.html", context)




def guest_entry_summary(request):
    year = request.GET.get('year')
    try:
        year = int(year)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid year'}, status=400)

    guests = GuestEntry.objects.filter(date_of_visit__year=year)

    # Total guests for the year
    total_count = guests.count()

    # Group by month and count
    month_counts = (
        guests.annotate(month=ExtractMonth('date_of_visit'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Build dict: {1: 5, 2: 10, ..., 12: 0}
    counts_dict = {month: 0 for month in range(1, 13)}
    for entry in month_counts:
        counts_dict[entry['month']] = entry['count']

    max_count = max(counts_dict.values())
    min_count = min(counts_dict.values())
    avg_count = sum(counts_dict.values()) // 12 if counts_dict else 0

    # Find month names
    max_months = [calendar.month_name[m] for m, c in counts_dict.items() if c == max_count]
    min_months = [calendar.month_name[m] for m, c in counts_dict.items() if c == min_count]

    # Just use the first if tie
    max_month = max_months[0] if max_months else "N/A"
    min_month = min_months[0] if min_months else "N/A"

    def percent(count):
        return round((count / max_count) * 100, 1) if max_count > 0 else 0

    data = {
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

    return JsonResponse(data)


def top_services_data(request):
    top_services = (
        GuestEntry.objects
        .values('service_attended')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Prepare data: list of dicts with service, count
    data = list(top_services)

    # Calculate total count of these top 10 to calculate % widths
    total = sum(item['count'] for item in data) or 1  # avoid division by zero

    # Add percentage to each
    for item in data:
        item['percent'] = round((item['count'] / total) * 100, 1)

    return JsonResponse({'services': data})




@login_required
def services_attended_chart(request):
    """AJAX endpoint for services attended chart."""

    queryset = GuestEntry.objects.all()  # No filtering by user

    qs = queryset.values('service_attended').annotate(count=Count('id')).order_by('-count')
    labels = [item['service_attended'] or "Not Specified" for item in qs]
    counts = [item['count'] for item in qs]

    return JsonResponse({'labels': labels, 'counts': counts})



@login_required
def channel_breakdown(request):
    """AJAX endpoint for channel of visit table."""
    
    queryset = GuestEntry.objects.all() 

    qs = queryset.values('channel_of_visit').annotate(count=Count('id')).order_by('-count')
    total = sum(item['count'] for item in qs)
    data = [
        {
            'label': item['channel_of_visit'] or 'Unknown',
            'count': item['count'],
            'percent': round((item['count'] / total) * 100, 2) if total else 0
        }
        for item in qs
    ]
    return JsonResponse(data, safe=False)





@login_required
def guest_list_view(request):
    """
    Guest List view with role-based access:
    - Regular users see only their created or assigned guests.
    - Admins see all guests, can filter by creator, assign guests.
    - Guests reassigned to someone else disappear from original user’s Guest List view.
    """
    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)
    day_name = now_in_wat.strftime('%A')
    time_str = now_in_wat.strftime('%I:%M %p')
    today_str = now_in_wat.strftime('%Y-%m-%d')
    is_staff_group = request.user.groups.filter(name='Admin').exists()

    show_welcome_modal = request.session.get('last_welcome_popup') != today_str
    if show_welcome_modal:
        request.session['last_welcome_popup'] = today_str

    user = request.user
    is_admin_group = user.groups.filter(name="Admin").exists() or user.is_superuser

    # Get filters
    filter_user_id = request.GET.get('user')
    search_query = request.GET.get('q')
    channel = request.GET.get('channel')
    status = request.GET.get('status')
    purpose = request.GET.get('purpose')
    service = request.GET.get('service')

    # Base queryset
    if is_admin_group:
        queryset = GuestEntry.objects.all()
        if filter_user_id and filter_user_id.isdigit():
            queryset = queryset.filter(created_by__id=filter_user_id)
    else:
        queryset = GuestEntry.objects.filter(
            Q(created_by=user, assigned_to__isnull=True) |
            Q(assigned_to=user)
        )

    # Apply filters
    if channel:
        queryset = queryset.filter(channel_of_visit__iexact=channel)
    if status:
        queryset = queryset.filter(status__iexact=status)
    if purpose:
        queryset = queryset.filter(purpose_of_visit__iexact=purpose)
    if service:
        queryset = queryset.filter(service_attended__iexact=service)
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(referrer_name__icontains=search_query)
        )

    queryset = queryset.annotate(
        report_count=Count('reports'),
        last_reported=Max('reports__report_date')
    ).order_by('-date_of_visit')

    # Pagination
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Add show_assigned_badge flag
    for guest in page_obj:
        guest.show_assigned_badge = (
            guest.assigned_to == user and guest.created_by != user
        )

    # Badge Rank Logic
    entry_count = queryset.count()
    badge = {
        "level": "Novice", "class": "bg-gradient-muted text-white",
        "bootstrap_icon": "bi bi-emoji-smile-fill fs-1",
        "message": f"Hi, {user.get_full_name()}!"
    }
    if entry_count >= 60:
        badge["level"] = "Expert"
    elif entry_count >= 30:
        badge["level"] = "Professional"
    elif entry_count >= 10:
        badge["level"] = "Apprentice"

    # Update message accordingly
    badge["message"] = f"Welcome back, {user.get_full_name()}!" if badge["level"] != "Novice" else badge["message"]

    # Context
    context = {
        'show_filters': True,
        'guests': page_obj,
        'page_obj': page_obj,
        'badge': badge,
        'entry_count': entry_count,
        'filter_user_id': int(filter_user_id) if filter_user_id and filter_user_id.isdigit() else None,
        'filter_service': service,
        'search_query': search_query,
        'export_query_string': urlencode({k: v for k, v in request.GET.items() if k != 'page'}),
        'is_admin_group': is_admin_group,
        'is_staff_group': user.groups.filter(name='Admin').exists(),
        'logged_in_user': user,
        'show_welcome_modal': show_welcome_modal,
        'day_name': day_name,
        'time_str': time_str,
        'channels': ['Billboard (Grammar School)', 'Billboard (Kosoko)', 'Facebook', 'Flyer', 'Instagram', 'Referral', 'Self', 'Visit', 'YouTube'],
        'statuses': ['Planted', 'Planted Elsewhere', 'Relocated', 'Work in Progress'],
        'purposes': ['Home Church', 'Occasional Visit', 'One-Time Visit', 'Special Programme Visit'],
        'services': ['Black Ball', 'Breakthrough Campaign', 'Breakthrough Festival', 'Code Red. Revival', 'Cross Over', 'Deep Dive', 'Family Hangout', 'Forecasting', 'Life Masterclass', 'Love Lounge', 'Midweek Recharge', 'Outreach', 'Quantum Leap', 'Recalibrate Marathon', 'Singles Connect', 'Supernatural Encounter'],
        'users': get_user_model().objects.filter(is_staff=False) if is_admin_group else None
    }

    return render(request, 'guests/guest_list.html', context)



def is_admin_group(user):
    return user.groups.filter(name='Admin').exists()

def can_edit_guest(user, guest):
    return (
        user == guest.created_by or
        user == guest.assigned_to or
        user.is_superuser or
        is_admin_group(user)
    )

def can_reassign(user):
    return user.is_superuser or is_admin_group(user)

@login_required
def create_guest(request):
    form = GuestEntryForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            guest = form.save(commit=False)
            guest.created_by = request.user
            guest.save()
            if 'save_add_another' in request.POST:
                return redirect('create_guest')
            return redirect('guest_list')

    return render(request, 'guests/guest_form.html', {
        'form': form,
        'edit_mode': False,
        'show_delete': False,
    })

@login_required
def edit_guest(request, pk):
    guest = get_object_or_404(GuestEntry, pk=pk)
    user = request.user

    if not can_edit_guest(user, guest):
        return redirect('guest_list')

    # Reassignment and user list (if allowed)
    reassign_allowed = can_reassign(user)
    all_users = get_user_model().objects.filter(is_active=True).order_by('first_name', 'last_name') if reassign_allowed else None

    if request.method == 'POST':
        # Handle Delete
        if 'delete_guest' in request.POST:
            if user == guest.created_by or user == guest.assigned_to or user.is_superuser or is_admin_group(user):
                guest.delete()
            return redirect('guest_list')

        # Handle Edit
        form = GuestEntryForm(request.POST, request.FILES, instance=guest)
        if form.is_valid():
            updated_guest = form.save(commit=False)

            # Reassign if permitted
            if reassign_allowed and 'assigned_to' in request.POST:
                assigned_id = request.POST.get('assigned_to')
                if assigned_id:
                    assigned_user = get_user_model().objects.filter(pk=assigned_id).first()
                    if assigned_user:
                        updated_guest.assigned_to = assigned_user

            # Clear picture if checked
            if 'clear_picture' in request.POST and guest.picture:
                guest.picture.delete(save=False)
                updated_guest.picture = None

            updated_guest.save()

            if 'save_add_another' in request.POST:
                return redirect('create_guest')
            return redirect('guest_list')
    else:
        form = GuestEntryForm(instance=guest)

    return render(request, 'guests/guest_form.html', {
        'form': form,
        'guest': guest,
        'edit_mode': True,
        'can_reassign': reassign_allowed,
        'all_users': all_users,
        'show_delete': True,
    })





@require_POST
@login_required
def update_guest_status(request, pk):
    """
    Updates a guest's follow-up status (via dropdown in guest_list).
    Only the creator or an admin can update.
    """
    guest = get_object_or_404(GuestEntry, pk=pk)

    if not (request.user.is_staff or guest.created_by == request.user):
        return redirect('guest_list')

    new_status = request.POST.get('status')
    if new_status in dict(GuestEntry.STATUS_CHOICES):
        guest.status = new_status
        guest.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def parse_flexible_date(date_str):
    """
    Try multiple date formats and return a valid `date` object or None.
    """
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except (ValueError, AttributeError):
            continue
    return None


def import_guests_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            username = row.get("created_by", "").strip()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.warning(request, f"User '{username}' not found. Skipping row.")
                continue

            try:
                dob = parse_flexible_date(row.get("date_of_birth"))
                dov = parse_flexible_date(row.get("date_of_visit"))

                GuestEntry.objects.create(
                    full_name=row.get("full_name", "").strip(),
                    title=row.get("title", "").strip(),
                    gender=row.get("gender", "").strip(),
                    phone_number=row.get("phone_number", "").strip(),
                    email=row.get("email", "").strip(),
                    date_of_birth=dob,
                    marital_status=row.get("marital_status", "").strip(),
                    home_address=row.get("home_address", "").strip(),
                    occupation=row.get("occupation", "").strip(),
                    date_of_visit=dov,
                    purpose_of_visit=row.get("purpose_of_visit", "").strip(),
                    channel_of_visit=row.get("channel_of_visit", "").strip(),
                    service_attended=row.get("service_attended", "").strip(),
                    referrer_name=row.get("referrer_name", "").strip(),
                    referrer_phone_number=row.get("referrer_phone_number", "").strip(),
                    message=row.get("message", "").strip(),
                    status=row.get("status", "").strip(),
                    created_by=user,
                )
            except Exception as e:
                messages.error(request, f"Error importing '{row.get('full_name')}' – {str(e)}")
                continue

        messages.success(request, "Guest list imported successfully.")
        return redirect("guest_list")

    messages.error(request, "Please upload a valid CSV file.")
    return redirect("guest_list")



import csv
from django.http import HttpResponse

def download_csv_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guest_import_template.csv"'

    writer = csv.writer(response)

    # Write header row
    writer.writerow([
        'full_name',               # Required
        'title',                   # Optional (Mr, Mrs, Miss, etc.)
        'gender',                  # Optional (Male, Female, Other)
        'phone_number',            # Optional
        'email',                   # Optional
        'date_of_birth',           # Optional (Any format like YYYY-MM-DD, DD/MM/YYYY, etc.)
        'marital_status',          # Optional
        'home_address',            # Optional
        'occupation',              # Optional
        'date_of_visit',           # Optional (Any format like YYYY-MM-DD, 24 July 2025, etc.)
        'purpose_of_visit',        # Optional
        'channel_of_visit',        # Optional (Flyer, Friend, Social Media, etc.)
        'service_attended',        # Optional (Sunday, Midweek, etc.)
        'referrer_name',           # Optional
        'referrer_phone_number',   # Optional
        'message',                 # Optional
        'status',                  # Optional (New, Returned, Not Interested, etc.)
        'created_by',              # Required (must match an existing username)
    ])

    # Optionally include one empty sample row
    writer.writerow([
        '', '', '', '', '',
        '', '', '', '',
        '', '', '', '',
        '', '', '', '', ''
    ])

    return response





@login_required
def export_csv(request):
    """
    Export filtered guest entries as CSV.
    - Admins can export all or filter by user.
    - Regular users can only export their own entries.
    - Respects service and search filters.
    """
    User = get_user_model()
    is_admin_group = request.user.groups.filter(name="Admin").exists() or request.user.is_superuser

    filter_user_id = request.GET.get('user')
    filter_service = request.GET.get('service')
    search_query = request.GET.get('q')

    # Base queryset
    if is_admin_group:
        guests = GuestEntry.objects.all()
        if filter_user_id and filter_user_id.isdigit():
            guests = guests.filter(created_by__id=filter_user_id)
    else:
        guests = GuestEntry.objects.filter(created_by=request.user)

    # Service filter
    if filter_service:
        guests = guests.filter(service_attended__iexact=filter_service)

    # Search filter
    if search_query:
        guests = guests.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(referrer_name__icontains=search_query)
        )

    # CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guest_entries.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Full Name', 'Phone Number', 'Email', 'Gender',
        'Date of Birth', 'Marital Status', 'Home Address',
        'Occupation', 'Date of Visit', 'Purpose of Visit',
        'Channel of Visit', 'Service Attended',
        'Referrer Name', 'Referrer Phone Number', 'Status',
        'Created By'
    ])

    for guest in guests:
        writer.writerow([
            guest.full_name,
            guest.phone_number,
            guest.email,
            guest.gender,
            guest.date_of_birth,
            guest.marital_status,
            guest.home_address,
            guest.occupation,
            guest.date_of_visit,
            guest.purpose_of_visit,
            guest.channel_of_visit,
            guest.service_attended,
            guest.referrer_name,
            guest.referrer_phone_number,
            guest.status,
            guest.created_by.get_full_name() if guest.created_by else '',
        ])

    return response


@login_required
def update_status_view(request, guest_id, status_key):
    guest = get_object_or_404(GuestEntry, id=guest_id)

    # Only allow if user is the creator or admin
    if request.user != guest.created_by and not request.user.is_superuser:
        return redirect('guest_list')  # or return an HTTP 403 Forbidden response

    guest.status = status_key
    guest.save()
    return redirect('guest_list')


@login_required
def export_guests_excel(request):
    is_admin_group = request.user.groups.filter(name="Admin").exists() or request.user.is_superuser
    filter_user_id = request.GET.get('user')
    filter_service = request.GET.get('service')
    search_query = request.GET.get('q')

    guests = GuestEntry.objects.all() if is_admin_group else GuestEntry.objects.filter(created_by=request.user)

    if filter_user_id and filter_user_id.isdigit():
        guests = guests.filter(created_by__id=filter_user_id)

    if filter_service:
        guests = guests.filter(service_attended__iexact=filter_service)

    if search_query:
        guests = guests.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(referrer_name__icontains=search_query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Guest Entries"

    headers = [
        'Full Name', 'Phone Number', 'Email', 'Gender',
        'Date of Birth', 'Marital Status', 'Home Address',
        'Occupation', 'Date of Visit', 'Purpose of Visit',
        'Channel of Visit', 'Service Attended',
        'Referrer Name', 'Referrer Phone Number', 'Status',
        'Created By'
    ]
    ws.append(headers)

    # Populate data rows
    guests = GuestEntry.objects.all()
    for guest in guests:
        ws.append([
            f"{guest.title} {guest.full_name}",
            guest.phone_number,
            guest.email,
            guest.gender,
            guest.date_of_birth.strftime('%Y-%m-%d') if guest.date_of_birth else "",
            guest.marital_status,
            guest.home_address,
            guest.occupation,
            guest.date_of_visit.strftime('%Y-%m-%d') if guest.date_of_visit else "",
            guest.purpose_of_visit,
            guest.channel_of_visit,
            guest.service_attended,
            guest.referrer_name,
            guest.referrer_phone_number,
            guest.status,
            guest.created_by.get_full_name() if guest.created_by else '',
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=guest_entries.xlsx'
    wb.save(response)
    return response



@login_required
def export_guests_pdf(request):
    guests = GuestEntry.objects.all()
    html = render_to_string('guests/guest_list_pdf.html', {'guests': guests})
    pdf_file = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="all_guests.pdf"'
    return response




@login_required
@user_passes_test(lambda u: u.is_staff)  # Only staff users can import
def import_guests_excel(request):
    if request.method == "POST":
        file = request.FILES.get("excel_file")
        if not file.name.endswith(".xlsx"):
            messages.error(request, "Only .xlsx files are supported.")
            return redirect("import_guests")

        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        headers = [cell.value for cell in sheet[1]]
        username_col = headers.index("Created By (Username)")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            try:
                created_by_username = row[username_col]
                created_by_user = User.objects.get(username=created_by_username)

                GuestEntry.objects.create(
                    title=row[0],
                    full_name=row[1],
                    gender=row[2],
                    phone_number=row[3],
                    email=row[4],
                    date_of_birth=row[5],
                    marital_status=row[6],
                    home_address=row[7],
                    occupation=row[8],
                    date_of_visit=row[9],
                    purpose_of_visit=row[10],
                    channel_of_visit=row[11],
                    service_attended=row[12],
                    referrer_name=row[13],
                    referrer_phone_number=row[14],
                    message=row[15],
                    created_by=created_by_user,
                )

            except User.DoesNotExist:
                messages.warning(request, f"User '{created_by_username}' not found. Skipping row.")
                continue
            except Exception as e:
                messages.error(request, f"Error importing row: {e}")
                continue

        messages.success(request, "Guests imported successfully.")
        return redirect("guest_list")

    return render(request, "guests/import_excel.html")


def get_week_start_end(target_date):
    start = target_date - timedelta(days=target_date.weekday())
    end = start + timedelta(days=6)
    return start, end





@login_required
def followup_report_page(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    today = localdate()
    guests = GuestEntry.objects.annotate(report_count=Count('reports'))

    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    error = None

    if request.method == 'POST' and 'submit_report' in request.POST:
        report_date = request.POST.get('date_of_visit') or localdate()
        note = request.POST.get('note')
        service_sunday = request.POST.get('service_sunday') == 'on'
        service_midweek = request.POST.get('service_midweek') == 'on'

        if not note:
            error = "Note field is required."
        else:
            try:
                FollowUpReport.objects.create(
                    guest=guest,
                    report_date=report_date,
                    note=note,
                    service_sunday=service_sunday,
                    service_midweek=service_midweek,
                    created_by=request.user,
                )
                return redirect('followup_report_page', guest_id=guest.id)
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                    error = "Duplicate dates are not allowed."
                else:
                    raise

    return render(request, 'guests/followup_report_page.html', {
        'guest': guest,
        'reports': reports,
        'page_obj': page_obj,
        'today': today,
        'error': error,
    })





def create_followup_report(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)

    if request.method == "POST":
        form = FollowUpReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.guest = guest
            report.created_by = request.user  # Automatically set creator
            report.save()
            messages.success(request, "Follow-up report created successfully.")
            return redirect('guest_detail', guest_id=guest.id)
    else:
        form = FollowUpReportForm()

    return render(request, 'guests/followup_form.html', {
        'form': form,
        'guest': guest
    })




"""
def get_guest_reports(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    report_data = [
        {
            'report_date': localtime(report.report_date).strftime('%Y-%m-%d'),
            'note': report.note,
            'sunday_attended': report.sunday_attended,
            'midweek_attended': report.midweek_attended,
        }
        for report in reports
    ]
    return JsonResponse({'reports': report_data})
"""


@login_required
def followup_history_view(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    return render(request, 'guests/followup_history.html', {
        'guest': guest,
        'reports': reports,
    })


def export_followup_reports_pdf(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')

    # Create a PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Guest Reports")

    styles = getSampleStyleSheet()
    elements = []

    # Custom title style
    title_style = ParagraphStyle(
        name='Title',
        fontSize=16,
        leading=24,
        alignment=1,  # Center
        spaceAfter=20,
    )

    # Optional Logo
    logo_path = os.path.join('static', 'your_logo.png')  # Adjust path
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=100, height=40)
        logo.hAlign = 'LEFT'
        elements.append(logo)

    # Title
    elements.append(Paragraph(f"Follow-Up Report for {guest.full_name}", title_style))
    elements.append(Spacer(1, 10))

    # Table header and data
    data = [['Date', 'Sunday', 'Midweek', 'Message', 'Created By']]
    for report in reports:
        created_by_name = report.created_by.get_full_name() if report.created_by else 'Unknown'
        data.append([
            report.report_date.strftime("%Y-%m-%d"),
            '✔️' if report.service_sunday else '',
            '✔️' if report.service_midweek else '',
            report.note or ''
        ])

    table = Table(data, colWidths=[80, 60, 60, 280, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="followup_reports_{guest.id}.pdf"'
    })



