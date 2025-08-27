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
            'placeholder': 'January 01 (Ignore Year)',
        }),
        help_text="Date of Birth."
    )

    date_of_visit = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={
            'type': 'date',
            'class': 'form-control',
            'autocomplete': 'off',
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],  # support input formats for validation
        required=False,
    )

    class Meta:
        model = GuestEntry
        exclude = ['assigned_to', 'status', 'custom_id']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@guest.gatewaynation'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08123xxxx89'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'January 01 (Ignore Year)',
                'autocomplete': 'off'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '3/4, Francis Aghedo Close, Off Isheri Road, Lagos'}),
            'date_of_visit': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'purpose_of_visit': forms.Select(attrs={'class': 'form-select'}),
            'channel_of_visit': forms.Select(attrs={'class': 'form-select'}),
            'service_attended': forms.Select(attrs={'class': 'form-select'}),
            'referrer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sis. Jane Doe'}),
            'referrer_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08123xxxx89'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write any additional notes about the Guest here...'}),
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
            'title': 'Title.',
            'picture': 'Profile Picture for the Guest.',
            'gender': 'Gender.',
            'full_name': 'Full Name.',
            'phone_number': 'Phone Number.',
            'email': 'Email Address.',
            'date_of_birth': 'Date of Birth.',
            'marital_status': 'Marital Status.',
            'home_address': 'Home Address.',
            'occupation': 'Occupation.',
            'date_of_visit': 'Date of Visit.',
            'purpose_of_visit': 'Purpose of Visit.',
            'channel_of_visit': 'How did the Guest found out about us?',
            'service_attended': 'What Service did the Guest Attend?',
            'referrer_name': 'Who referred the Guest?',
            'referrer_phone_number': 'Referrer\'s Phone Number.',
            'message': 'Additional Notes.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        


        # Fields that should allow blank without showing '---------' or 'None'
        select_fields = ['title', 'marital_status', 'gender', 'purpose_of_visit',
                         'channel_of_visit', 'service_attended', 'status']

        for field_name in select_fields:
            if field_name in self.fields:
                # Replace default empty label with a real blank choice
                choices = list(self.fields[field_name].choices)
                if choices and choices[0][0] == '':
                    # Replace first choice (usually '---------') with empty
                    choices[0] = ("", "")
                else:
                    # If no blank exists, prepend one
                    choices = [("", "")] + choices
                self.fields[field_name].choices = choices

        # Format initial date_of_visit to ISO
        if self.instance and self.instance.date_of_visit:
            self.fields['date_of_visit'].initial = self.instance.date_of_visit.strftime('%Y-%m-%d')

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
        exclude = ['guest', 'created_by', 'created_at']
        fields = ['report_date', 'note', 'service_sunday', 'service_midweek']
        widgets = {
            'report_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write follow-up note here...'
            }),
            'service_sunday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'service_midweek': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        self.guest = kwargs.pop('guest', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        report_date = cleaned_data.get('report_date')

        if FollowUpReport.objects.filter(guest=self.guest, report_date=report_date).exists():
            raise ValidationError("You already submitted a report for this date.")

        return cleaned_data



    

