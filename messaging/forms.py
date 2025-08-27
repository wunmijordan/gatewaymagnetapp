from django import forms
from .models import GuestMessage
from guests.models import GuestEntry


class BulkMessageForm(forms.ModelForm):
    guest_status = forms.ChoiceField(
        choices=GuestEntry.STATUS_CHOICES,
        label="Select Guest Status",
        widget=forms.Select(attrs={
            'class': 'form-select bg-grey text-white border-0'
        })
    )

    class Meta:
        model = GuestMessage
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
