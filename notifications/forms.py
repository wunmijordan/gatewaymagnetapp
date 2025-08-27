# notifications/forms.py
from django import forms
from .models import UserSettings

class UserSettingsForm(forms.ModelForm):
  class Meta:
      model = UserSettings
      fields = ['notification_sound', 'vibration_enabled']
      widgets = {
          'notification_sound': forms.Select(attrs={'class': 'form-select'}),
          'vibration_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
      }