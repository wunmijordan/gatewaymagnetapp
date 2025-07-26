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
from django.utils.timezone import localtime, now
import pytz
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.db.models import Count, Max
from django.template.loader import get_template
import weasyprint
#from .utils import get_week_start_end
from guests.models import GuestEntry
from django.utils.dateparse import parse_date


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

    return redirect('dashboard')





@login_required
def dashboard_view(request):
    """
    Dashboard view with role-based access:
    - Regular users see only their created or assigned guests.
    - Admins see all guests, can filter by creator, assign guests.
    - Guests reassigned to someone else disappear from original user’s dashboard.
    """
    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)
    today_str = now_in_wat.strftime('%Y-%m-%d')
    is_staff_group = request.user.groups.filter(name='Admin').exists()

    # Welcome popup logic
    show_welcome_modal = request.session.get('last_welcome_popup') != today_str
    if show_welcome_modal:
        request.session['last_welcome_popup'] = today_str

    day_name = now_in_wat.strftime('%A')
    time_str = now_in_wat.strftime('%I:%M %p')

    User = get_user_model()
    is_admin_group = request.user.groups.filter(name="Admin").exists() or request.user.is_superuser

    # Filters
    filter_user_id = request.GET.get('user')
    filter_service = request.GET.get('service')
    search_query = request.GET.get('q')
    status_filter = request.GET.get('status')

    # Base queryset
    if is_admin_group:
        guests = GuestEntry.objects.all()
        if filter_user_id and filter_user_id.isdigit():
            guests = guests.filter(created_by__id=filter_user_id)
    else:
        # Show only guests user created or was assigned to
        guests = GuestEntry.objects.filter(
            Q(created_by=request.user, assigned_to__isnull=True) |
            Q(assigned_to=request.user)
        )

    # Add report annotations
    guests = guests.annotate(
        report_count=Count('followup_reports'),
        last_reported=Max('followup_reports__report_date')
    )

    # Additional filters
    if filter_service:
        guests = guests.filter(service_attended__iexact=filter_service)
    if status_filter:
        guests = guests.filter(status__iexact=status_filter)
    if search_query:
        guests = guests.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(referrer_name__icontains=search_query)
        )

    guests = guests.order_by('-date_of_visit')

    # Add 'show_assigned_badge' flag for frontend
    for guest in guests:
        guest.show_assigned_badge = (
            guest.assigned_to == request.user and guest.created_by != request.user
        )

    # Pagination
    paginator = Paginator(guests, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Badge Rank Logic
    entry_count = guests.count()
    if entry_count >= 60:
        badge = {
            "level": "Expert", "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-trophy-fill fs-1",
            "message": f"Welcome back, {request.user.get_full_name()}. You're a rockstar officer. Keep up the good work!"
        }
    elif entry_count >= 30:
        badge = {
            "level": "Professional", "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-award-fill fs-1",
            "message": f"Welcome, {request.user.get_full_name()}. You're a top-level officer. More to go!"
        }
    elif entry_count >= 10:
        badge = {
            "level": "Apprentice", "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-emoji-smile-fill fs-1",
            "message": f"Hello, {request.user.get_full_name()}. You're a middle-level officer. Lots more ahead!"
        }
    else:
        badge = {
            "level": "Novice", "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-emoji-neutral-fill fs-1",
            "message": f"Hi, {request.user.get_full_name()}. You're still a long way up. Keep at it!"
        }

    # Services list for filters
    services = GuestEntry.objects.values_list('service_attended', flat=True).distinct().order_by('service_attended')

    # Export Querystring
    current_query_params = request.GET.copy()
    current_query_params.pop('page', None)
    export_query_string = urlencode(current_query_params)

    context = {
        'guests': page_obj,
        'page_obj': page_obj,
        'users': User.objects.all() if is_admin_group else None,
        'services': services,
        'badge': badge,
        'entry_count': entry_count,
        'filter_user_id': int(filter_user_id) if filter_user_id and filter_user_id.isdigit() else None,
        'filter_service': filter_service,
        'search_query': search_query,
        'export_query_string': export_query_string,
        'is_admin_group': is_admin_group,
        'is_staff_group': is_staff_group,
        'logged_in_user': request.user,
        'show_welcome_modal': show_welcome_modal,
        'day_name': day_name,
        'time_str': time_str,
    }

    if request.user.groups.filter(name='Admin').exists():
        context['users'] = User.objects.filter(is_staff=False)  # only for dropdown

    return render(request, 'guests/dashboard.html', context)




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
            return redirect('dashboard')

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
        return redirect('dashboard')

    # Reassignment and user list (if allowed)
    reassign_allowed = can_reassign(user)
    all_users = get_user_model().objects.filter(is_active=True).order_by('first_name', 'last_name') if reassign_allowed else None

    if request.method == 'POST':
        # Handle Delete
        if 'delete_guest' in request.POST:
            if user == guest.created_by or user.is_superuser or is_admin_group(user):
                guest.delete()
            return redirect('dashboard')

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
            return redirect('dashboard')
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
    Updates a guest's follow-up status (via dropdown in dashboard).
    Only the creator or an admin can update.
    """
    guest = get_object_or_404(GuestEntry, pk=pk)

    if not (request.user.is_staff or guest.created_by == request.user):
        return redirect('dashboard')

    new_status = request.POST.get('status')
    if new_status in dict(GuestEntry.STATUS_CHOICES):
        guest.status = new_status
        guest.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def import_guests_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            username = row.get("created_by")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.warning(request, f"User '{username}' not found. Skipping row.")
                continue

            try:
                GuestEntry.objects.create(
                    full_name=row.get("full_name"),
                    title=row.get("title"),
                    gender=row.get("gender"),
                    phone_number=row.get("phone_number"),
                    email=row.get("email"),
                    date_of_birth=parse_date(row.get("date_of_birth")) if row.get("date_of_birth") else None,
                    marital_status=row.get("marital_status"),
                    home_address=row.get("home_address"),
                    occupation=row.get("occupation"),
                    date_of_visit=parse_date(row.get("date_of_visit")) if row.get("date_of_visit") else None,
                    purpose_of_visit=row.get("purpose_of_visit"),
                    channel_of_visit=row.get("channel_of_visit"),
                    service_attended=row.get("service_attended"),
                    referrer_name=row.get("referrer_name"),
                    referrer_phone_number=row.get("referrer_phone_number"),
                    message=row.get("message"),
                    status=row.get("status"),
                    created_by=user
                )
            except Exception as e:
                messages.error(request, f"Error importing row: {row.get('full_name')} – {str(e)}")
                continue

        messages.success(request, "Guest list imported successfully.")
        return redirect("dashboard")

    messages.error(request, "Please upload a valid CSV file.")
    return redirect("dashboard")


def download_csv_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guest_template.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'full_name', 'title', 'gender', 'phone_number', 'email',
        'date_of_birth', 'marital_status', 'home_address', 'occupation',
        'date_of_visit', 'purpose_of_visit', 'channel_of_visit', 'service_attended',
        'referrer_name', 'referrer_phone_number', 'message', 'status', 'created_by'
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
        return redirect('dashboard')  # or return an HTTP 403 Forbidden response

    guest.status = status_key
    guest.save()
    return redirect('dashboard')


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
        return redirect("dashboard")

    return render(request, "guests/import_excel.html")


def get_week_start_end(target_date):
    start = target_date - timedelta(days=target_date.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_followup_form(request, guest_id):
    guest = get_object_or_404(GuestEntry, pk=guest_id)
    form = FollowUpReportForm()  # Use correct form class

    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')

    html = render_to_string('guests/followup_form_modal_content.html', {
        'form': form,
        'guest': guest,
        'past_reports': reports
    }, request=request)

    return JsonResponse({'form_html': html})


@csrf_protect
@login_required
def submit_followup_report(request, guest_id):
    if request.method == 'POST':
        guest = get_object_or_404(GuestEntry, id=guest_id)
        form = FollowUpReportForm(request.POST)

        if form.is_valid():
            report_date = form.cleaned_data['report_date']
            start_week, end_week = get_week_start_end(report_date)

            exists = FollowUpReport.objects.filter(
                guest=guest,
                report_date__range=(start_week, end_week)
            ).exists()

            if exists:
                return JsonResponse({
                    'status': 'error',
                    'message': 'A report for this week already exists.'
                }, status=400)

            followup = form.save(commit=False)
            followup.guest = guest
            followup.created_by = request.user
            followup.save()

            # ✅ Add report count to the response
            report_count = FollowUpReport.objects.filter(guest=guest).count()

            return JsonResponse({
                'status': 'success',
                'message': 'Report submitted successfully.',
                'report_count': report_count  # 👈 required by your JS
            })

        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)




def get_guest_reports(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    report_data = [
        {
            'report_date': localtime(report.report_date).strftime('%Y-%m-%d'),
            'notes': report.notes,
            'sunday_attended': report.sunday_attended,
            'midweek_attended': report.midweek_attended,
        }
        for report in reports
    ]
    return JsonResponse({'reports': report_data})



@login_required
def followup_history_view(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    return render(request, 'guests/followup_history.html', {
        'guest': guest,
        'reports': reports,
    })

@login_required
def delete_followup_report(request, report_id):
    report = get_object_or_404(FollowUpReport, id=report_id)
    if request.method == 'POST':
        report.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
def edit_followup_report(request, report_id):
    report = get_object_or_404(FollowUpReport, id=report_id)
    if request.method == 'POST':
        form = FollowUpReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = FollowUpReportForm(instance=report)
        form_html = render_to_string('guests/edit_followup_form.html', {'form': form, 'report': report}, request=request)
        return JsonResponse({'form_html': form_html})

@login_required
def export_followup_report_pdf(request, guest_id):
    guest = get_object_or_404(GuestEntry, id=guest_id)
    reports = FollowUpReport.objects.filter(guest=guest).order_by('-report_date')
    html = render_to_string('guests/followup_report_pdf.html', {'guest': guest, 'reports': reports})
    pdf_file = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{guest.full_name}_followup_reports.pdf"'
    return response


