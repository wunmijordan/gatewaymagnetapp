from django.http import HttpResponse
from django.views.decorators.http import require_GET
import os
from django.shortcuts import render


@require_GET
def service_worker(request):
    sw_path = os.path.join(
        os.path.dirname(__file__), 
        'static', 
        'serviceworker.js'
    )
    with open(sw_path, 'r') as sw_file:
        response = HttpResponse(sw_file.read(), content_type='application/javascript')
    return response



def offline_page(request):
    return render(request, 'offline.html')
