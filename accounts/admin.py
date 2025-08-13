from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile
from django.utils.html import format_html

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('full_name', 'phone_number', 'image')  # show full_name instead of first/last
    readonly_fields = ()  # make empty tuple if you want it editable

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    # optionally display full_name in user list view
    def full_name(self, obj):
        return obj.profile.full_name if hasattr(obj, 'profile') else ''
    full_name.short_description = 'Full Name'

    list_display = ('username', 'full_name', 'email', 'is_staff', 'is_active')
    list_select_related = ('profile',)  # optimize queries

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'image_display')
    search_fields = ('user__username', 'full_name')  # search by full_name

    @admin.display(description='Full Name')
    def full_name(self, obj):
        return obj.full_name

    @admin.display(description='Image')
    def image_display(self, obj):
        try:
            if obj.image and obj.image.url:
                return format_html(
                    '<img src="{}" width="40" height="40" style="border-radius:50%"/>',
                    obj.image.url
                )
        except Exception:
            pass
        return "-"
