from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BulkMessageForm
from .models import GuestMessage
from guests.models import GuestEntry
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BulkMessageForm
from .models import GuestMessage
from guests.models import GuestEntry


@login_required
def send_bulk_message(request):
  if request.method == "POST":
      form = BulkMessageForm(request.POST)
      if form.is_valid():
          message = form.save(commit=False)
          message.sender = request.user
          message.save()

          # Filter recipients by selected guest status
          status = form.cleaned_data['guest_status']
          recipients = GuestEntry.objects.filter(status=status)
          message.recipients.set(recipients)

          # Send the message
          message.send()

          messages.success(request, f"Message sent to {recipients.count()} guests.")
      else:
          messages.error(request, "Form submission failed. Please check your inputs.")

  return redirect('guest_list')  # redirect back to dashboard/guest list



def send_guest_message(request, guest_id):
  guest = get_object_or_404(GuestEntry, id=guest_id)
  user = request.user

  # Permission check
  if user.role not in ['Superuser', 'Admin', 'Message Manager'] and guest.assigned_to != user:
    messages.error(request, "You cannot message this guest.")
    return redirect('dashboard')

  if request.method == 'POST':
    body = request.POST.get('body', '')
    subject = request.POST.get('subject', 'No Subject')
    recipient_id = request.POST.get('recipient_id')

    recipient = get_object_or_404(GuestEntry, id=recipient_id)

    message_obj = GuestMessage.objects.create(sender=user, subject=subject, body=body)
    message_obj.recipients.add(recipient)
    message_obj.send()

    messages.success(request, f"Message sent to {recipient.full_name}")
    return redirect('dashboard')



def get_guests_by_status(request):
  """
  Return guests as JSON based on selected statuses.
  Only accessible to users with bulk messaging rights.
  """
  if request.user.role not in ['Superuser', 'Admin', 'Message Manager']:
    return JsonResponse({'error': 'Unauthorized'}, status=403)

  status_filters = request.GET.getlist('status[]')
  queryset = GuestEntry.objects.all()
  if status_filters:
    queryset = queryset.filter(status__in=status_filters)

  guests = [{'id': g.id, 'name': g.full_name} for g in queryset]
  return JsonResponse({'guests': guests})
