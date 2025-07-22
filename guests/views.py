from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import GuestEntry, FollowUpReport
from .forms import GuestEntryForm, FollowUpReportForm
import csv
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



@login_required
def dashboard_view(request):
    """
    Dashboard view:
    - Admins and superusers see all entries and filter by user.
    - Regular users see only their own entries.
    - Supports filtering by service and search.
    - Badge rank based on number of entries.
    """

    tz = pytz.timezone('Africa/Lagos')
    now_in_wat = localtime(now(), timezone=tz)  # current time in WAT
    
    today_str = now_in_wat.strftime('%Y-%m-%d')
    last_popup_shown = request.session.get('last_welcome_popup', '')
    
    show_welcome_modal = (last_popup_shown != today_str)
    if show_welcome_modal:
        request.session['last_welcome_popup'] = today_str
    
    day_name = now_in_wat.strftime('%A')
    time_str = now_in_wat.strftime('%I:%M %p')  # 12-hour format with AM/PM


    User = get_user_model()
    is_admin_group = request.user.groups.filter(name="Admin").exists() or request.user.is_superuser

    # Get filter parameters
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

    guests = guests.annotate(
        report_count=Count('followup_reports'),
        last_reported=Max('followup_reports__report_date')
    )

    # Apply service filter
    if filter_service:
        guests = guests.filter(service_attended__iexact=filter_service)

    status_filter = request.GET.get('status')
    if status_filter:
        guests = guests.filter(status__iexact=status_filter)
        # If the user is not in the admin group, filter by their own entries
        #if not is_admin_group:
         #   guests = guests.filter(created_by=request.user)

    # Apply search filter
    if search_query:
        guests = guests.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(referrer_name__icontains=search_query)
        )

    guests = guests.order_by('-date_of_visit')

    # Determine selected user for badge message
    filtered_user = (
        get_object_or_404(User, id=filter_user_id)
        if is_admin_group and filter_user_id and filter_user_id.isdigit()
        else request.user
    )
    selected_user = filtered_user if is_admin_group else request.user
    logged_in_user = request.user
    entry_count = guests.count()

    # Pagination (6 per page)
    paginator = Paginator(guests, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Badge logic
    if entry_count >= 60:
        badge = {
            "level": "Expert",
            "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-trophy-fill fs-1",
            "message": f"Welcome back, {request.user.get_full_name()}. You're a rockstar officer. Keep up the good work!"
        }
    elif entry_count >= 30:
        badge = {
            "level": "Professional",
            "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-award-fill fs-1",
            "message": f"Welcome, {request.user.get_full_name()}. You're a top-level officer. More to go!"
        }
    elif entry_count >= 10:
        badge = {
            "level": "Apprentice",
            "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-emoji-smile-fill fs-1",
            "message": f"Hello, {request.user.get_full_name()}. You're a middle-level officer. Lots more ahead!"
        }
    else:
        badge = {
            "level": "Novice",
            "class": "bg-gradient-muted text-white",
            "bootstrap_icon": "bi bi-emoji-neutral-fill fs-1",
            "message": f"Hi, {request.user.get_full_name()}. You're still a long way up. Keep at it!"
        }

    # Get unique services for dropdown
    services = GuestEntry.objects.values_list('service_attended', flat=True).distinct().order_by('service_attended')

    # Prepare querystring for CSV export
    current_query_params = request.GET.copy()
    if 'page' in current_query_params:
        del current_query_params['page']  # Don't include pagination in CSV
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
        'logged_in_user': request.user,  # <-- for welcome message
        'show_welcome_modal': show_welcome_modal,
        'day_name': day_name,
        'time_str': time_str,
    }

    return render(request, 'guests/dashboard.html', context)






@login_required
def guest_entry_view(request, pk=None):
    """
    Handles guest entry create/edit.
    """
    guest = get_object_or_404(GuestEntry, pk=pk) if pk else None

    if guest and not (request.user.is_staff or guest.created_by == request.user):
        return redirect('dashboard')  # Permission denied

    if request.method == 'POST':
        form = GuestEntryForm(request.POST, request.FILES, instance=guest)
        if form.is_valid():
            entry = form.save(commit=False)

            if not guest:
                entry.created_by = request.user

            # Clear picture if user requested
            if 'clear_picture' in request.POST and guest and guest.picture:
                guest.picture.delete(save=False)
                entry.picture = None

            entry.save()

            if 'save_return' in request.POST:
                return redirect('dashboard')
            elif 'save_add_another' in request.POST:
                return redirect('guest_entry')
        # else: form will re-render with errors
    else:
        form = GuestEntryForm(instance=guest)

    return render(request, 'guests/guest_form.html', {
        'form': form,
        'guest': guest
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
def import_guests_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):
            full_name = row[0]
            phone_number = row[1]
            # ... extract other fields as needed

            GuestEntry.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                created_by=request.user,
                # Map the rest...
            )
        messages.success(request, "Guests imported successfully.")
    return redirect('dashboard')


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


