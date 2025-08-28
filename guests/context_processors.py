from .models import GuestEntry

def superuser_guests(request):
    if request.user.is_authenticated and request.user.is_superuser:
        guests = GuestEntry.objects.all().order_by('-custom_id')
    else:
        guests = []
    return {'superuser_guests': guests}
