from django.contrib import admin
from .models import GuestEntry, FollowUpReport, SocialMediaEntry


class SocialMediaEntryInline(admin.TabularInline):
    model = SocialMediaEntry
    extra = 1
    min_num = 0
    can_delete = True


@admin.register(GuestEntry)
class GuestEntryAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'custom_id', 'date_of_visit', 'service_attended',
        'status', 'assigned_to'
    )
    list_filter = ('status', 'service_attended', 'assigned_to')
    search_fields = ('full_name', 'phone_number', 'email', 'referrer_name')
    inlines = [SocialMediaEntryInline]

    fieldsets = (
        (None, {
            'fields': (
                'picture', 'title', 'full_name', 'gender', 'phone_number', 'email',
                'date_of_birth', 'marital_status', 'home_address', 'occupation',
                'date_of_visit', 'purpose_of_visit', 'channel_of_visit',
                'service_attended', 'referrer_name', 'referrer_phone_number',
                'message', 'status', 'assigned_to'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role in ['Admin', 'Message Manager']:
            return qs
        # Team members see only assigned guests
        return qs.filter(assigned_to=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role in ['Admin', 'Message Manager']:
            return True
        if obj and obj.assigned_to == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role in ['Admin', 'Message Manager']:
            return True
        if obj and obj.assigned_to == request.user:
            return True
        return False

    def save_model(self, request, obj, form, change):
        """
        Ensure only superuser/admin/message manager can assign guests.
        Team members auto-assign to themselves if creating a guest.
        """
        if not change and request.user.role not in ['Admin', 'Superuser', 'Message Manager']:
            obj.assigned_to = request.user
        super().save_model(request, obj, form, change)


@admin.register(FollowUpReport)
class FollowUpReportAdmin(admin.ModelAdmin):
    list_display = (
        'guest', 'report_date', 'created_by',
        'service_sunday', 'service_midweek', 'reviewed'
    )
    list_filter = ('report_date', 'service_sunday', 'service_midweek', 'reviewed')
    search_fields = ('guest__full_name', 'note', 'created_by__username')
    list_editable = ('reviewed',)
