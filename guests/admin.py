from django.contrib import admin
from .models import GuestEntry
from .models import FollowUpReport


@admin.register(GuestEntry)
class GuestEntryAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'date_of_visit', 'service_attended',
        'status', 'created_by', 'assigned_to'
    )
    list_filter = ('status', 'service_attended', 'created_by')
    search_fields = ('full_name', 'phone_number', 'email', 'referrer_name')
    raw_id_fields = ('created_by',)

    fieldsets = (
        (None, {
            'fields': (
                'picture', 'title', 'full_name', 'gender', 'phone_number', 'email',
                'date_of_birth', 'marital_status', 'home_address', 'occupation',
                'date_of_visit', 'purpose_of_visit', 'channel_of_visit',
                'service_attended', 'referrer_name', 'referrer_phone_number',
                'message', 'status', 'created_by', 'assigned_to'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow superusers and staff to see all, otherwise only user’s own entries
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        # Allow superuser or creator to edit
        if request.user.is_superuser or (obj and obj.created_by == request.user):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Allow superuser or creator to delete
        if request.user.is_superuser or (obj and obj.created_by == request.user):
            return True
        return super().has_delete_permission(request, obj)


@admin.register(FollowUpReport)
class FollowUpReportAdmin(admin.ModelAdmin):
    list_display = ('guest', 'report_date', 'created_by', 'service_sunday', 'service_midweek', 'reviewed')
    list_filter = ('report_date', 'service_sunday', 'service_midweek', 'reviewed')
    search_fields = ('guest__full_name', 'note', 'created_by__username')
    list_editable = ('reviewed',)  # Allows toggling directly from the list page
