from django import forms
from .models import GuestEntry
from django.core.exceptions import ValidationError
import datetime
from .models import FollowUpReport

class GuestEntryForm(forms.ModelForm):

    date_of_birth = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. January 01',
        }),
        help_text="Enter month and day only, e.g., January 01"
    )

    class Meta:
        model = GuestEntry
        exclude = ['created_by', 'assigned_to', 'status']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'e.g. January 01',
                'autocomplete': 'off'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_visit': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purpose_of_visit': forms.Select(attrs={'class': 'form-select'}),
            'channel_of_visit': forms.Select(attrs={'class': 'form-select'}),
            'service_attended': forms.Select(attrs={'class': 'form-select'}),
            'referrer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'referrer_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'followup_status': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'title': 'Title',
            'picture': 'Profile Picture',
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'date_of_birth': 'Date of Birth',
            'marital_status': 'Marital Status',
            'occupation': 'Occupation',
            'date_of_visit': 'Date of Visit',
            'purpose_of_visit': 'Purpose of Visit',
            'channel_of_visit': 'Channel of Visit',
            'service_attended': 'Service Attended',
            'referrer_name': 'Referrer Name',
            'referrer_phone_number': 'Referrer Phone Number',
        }
        help_texts = {
            'full_name': 'Enter the full name of the guest.',
            'phone_number': 'Enter a valid phone number.',
            'email': 'Optional: Enter a valid email address.',
            'date_of_birth': 'Ex: January 01 (year will be ignored).',
            'marital_status': 'Select marital status if applicable.',
            'occupation': 'Optional: Enter occupation details.',
            'date_of_visit': 'Select the date of visit.',
            'purpose_of_visit': 'Select the purpose of visit from the list.',
            'channel_of_visit': 'Select how the guest found out about us.',
            'service_attended': 'Select the service attended during the visit.',
            'referrer_name': 'Optional: Name of the person who referred the guest.',
            'referrer_phone_number': 'Optional: Phone number of the referrer.'
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_date_of_birth(self):
        dob_raw = self.cleaned_data.get('date_of_birth')
        if not dob_raw:
            return None

        try:
            # Try parsing format like "January 01"
            dob_parsed = datetime.datetime.strptime(dob_raw, "%B %d").date()
            # Force a default year (e.g., 1900)
            dob_parsed = dob_parsed.replace(year=1900)
            return dob_parsed
        except ValueError:
            raise forms.ValidationError("Enter date in format: January 01")


class FollowUpReportForm(forms.ModelForm):
    class Meta:
        model = FollowUpReport
        fields = ['report_date', 'notes', 'attended_sunday', 'attended_midweek']
        widgets = {
            'report_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write follow-up notes here...'
            }),
            'attended_Sunday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attended_Midweek': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


