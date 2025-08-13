# accounts/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField(required=True, label="Profile Picture")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'is_staff']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                image=self.cleaned_data.get('image')  # Save uploaded image
            )

        return user


class UserEditForm(forms.ModelForm):
    # Pull phone_number and image from related Profile
    full_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)
    image = forms.ImageField(required=False, label="Profile Picture")
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "phone_number", "groups"]

    def __init__(self, *args, **kwargs):
        user = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        if user:
            profile = getattr(user, "profile", None)
            if profile:
                self.fields["phone_number"].initial = profile.phone_number
                self.fields["image"].initial = profile.image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data.get("phone_number")
            if self.cleaned_data.get("image"):
                profile.image = self.cleaned_data.get("image")
            profile.save()
            # Update groups
            user.groups.set(self.cleaned_data.get("groups"))
        return user


from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}"

    def save(self, commit=True):
        full_name = self.cleaned_data.get('full_name', '')
        first_name, *last_name = full_name.split(' ', 1)
        self.instance.first_name = first_name
        self.instance.last_name = last_name[0] if last_name else ''
        return super().save(commit=commit)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'image']
