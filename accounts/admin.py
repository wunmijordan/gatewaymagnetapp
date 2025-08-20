from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm




@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'full_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'image_display')
    ordering = ('username',)
    readonly_fields = ('image_display',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'full_name', 'email', 'phone_number', 'image',
            'title', 'marital_status', 'department', 'address', 'date_of_birth'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'full_name', 'phone_number', 'image',
                'password', 'confirm_password',
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
                'title', 'marital_status', 'department', 'address', 'date_of_birth',
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Provide current_user to the form so permissions logic works.
        """
        if obj is None:
            kwargs['form'] = self.add_form
        else:
            kwargs['form'] = self.form

        form_class = super().get_form(request, obj, **kwargs)

        class WrappedForm(form_class):
            def __init__(self_inner, *args, **kw):
                # Pass current_user safely if form expects it
                if 'current_user' in kw:
                    kw.pop('current_user')
                super().__init__(*args, **kw)

        return WrappedForm

    # ✅ Image preview
    def image_display(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%" />', obj.image.url)
        return "-"
    image_display.short_description = "Profile Picture"
