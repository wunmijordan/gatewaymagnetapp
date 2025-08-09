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

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Unregister original User admin and register custom one with inline Profile
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Profile independently if you want (without online status fields)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'image')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    @admin.display(description='Image')
    def image(self, obj):
        """Show user image if available."""
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%"/>',
                obj.image.url
            )
        return "-"
