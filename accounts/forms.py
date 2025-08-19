from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        help_text="Username.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Username'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Group"
    )
    is_staff = forms.BooleanField(
        required=False,
        label="Staff Status",
    )
    is_active = forms.BooleanField(
        required=False,
        label="Staff Status",
    )
    is_superuser = forms.BooleanField(
        required=False,
        label="Staff Status",
    )

    class Meta:
        model = CustomUser
        fields = [
            'image', 'title', 'full_name', 'email', 'username',
            'password', 'confirm_password', 'phone_number', 'date_of_birth',
            'address', 'marital_status', 'department', 'group', 'is_active', 'is_staff', 'is_superuser'
        ]

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@magnet.gatewaynation'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08123xxxx89'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'January 01 (Ignore Year)',
                'autocomplete': 'off'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '3/4, Francis Aghedo Close, Off Isheri Road, Lagos'}),
        }

        help_texts = {
            'title': 'Title.',
            'image': 'Profile Picture.',
            'full_name': 'Full Name.',
            'phone_number': 'Phone Number.',
            'email': 'Email Address.',
            'date_of_birth': 'Date of Birth.',
            'marital_status': 'Marital Status.',
            'address': 'Home Address.',
            'department': 'Department.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not password or not confirm_password:
            raise ValidationError("Both password fields are required.")
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.groups.set([self.cleaned_data.get("group")])
        return user

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Hide sensitive fields for non-superusers
        if self.current_user and not self.current_user.is_superuser:
            for f in ['is_staff', 'is_superuser']:
                self.fields.pop(f, None)

        # Default group to "Team Member" (only for creation, i.e. no instance pk)
        if not self.instance.pk:  
            try:
                default_group = Group.objects.get(name="Team Member")
                self.fields['group'].initial = default_group.id
            except Group.DoesNotExist:
                pass  # safe fallback if group doesn't exist


class CustomUserChangeForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        help_text="Username.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Username'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter New Password'}),
        required=False
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        required=False
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Group"
    )
    # Add admin fields as checkboxes
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Staff Status"
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Active"
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Superuser"
    )

    class Meta:
        model = CustomUser
        fields = [
            'image', 'title', 'full_name', 'email', 'username', 'password', 'confirm_password',
            'phone_number', 'date_of_birth', 'address', 'marital_status', 'department',
            'group', 'is_staff', 'is_active', 'is_superuser'
        ]

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@magnet.gatewaynation'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08123xxxx89'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'January 01 (Ignore Year)',
                'autocomplete': 'off'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '3/4, Francis Aghedo Close, Off Isheri Road, Lagos'}),
        }

        help_texts = {
            'title': 'Title.',
            'image': 'Profile Picture.',
            'full_name': 'Full Name.',
            'phone_number': 'Phone Number.',
            'email': 'Email Address.',
            'date_of_birth': 'Date of Birth.',
            'marital_status': 'Marital Status.',
            'address': 'Home Address.',
            'department': 'Department.',
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.edit_mode = kwargs.pop('edit_mode', False)  # <- add this
        super().__init__(*args, **kwargs)

        # Only apply frontend restrictions if current_user is explicitly passed
        if self.current_user:
            # Disable or hide is_staff for non-superuser admin-group users
            if not self.current_user.is_superuser:
                self.fields['is_staff'].disabled = True  # readonly

        # Pre-select user group
        if self.instance.pk:
            groups = self.instance.groups.all()
            self.fields['group'].initial = groups.first().id if groups.exists() else None

            # Pre-select user_permissions
            #self.fields['user_permissions'].initial = self.instance.user_permissions.all()

        # FRONTEND restrictions
        if self.edit_mode and self.current_user:
            if not self.current_user.is_superuser:
                # Non-superuser staff: hide / disable sensitive fields
                for f in ['is_staff', 'is_superuser']:
                    if f in self.fields:
                        self.fields.pop(f)  # completely hide these fields

        # Preselect current group
        if self.instance.pk:
            groups = self.instance.groups.all()
            if groups.exists():
                self.fields['group'].initial = groups.first().id

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.password = make_password(password)

        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            if group:
                user.groups.set([group])
            else:
                user.groups.clear()

            # Assign permissions (only if field exists, i.e., superuser)
            #if 'user_permissions' in self.cleaned_data:
            #    user.user_permissions.set(self.cleaned_data.get("user_permissions"))
        return user
