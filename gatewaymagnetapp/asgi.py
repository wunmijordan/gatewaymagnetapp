"""
ASGI config for gatewaymagnetapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# gatewaymagnetapp/asgi.py
import os

# MUST come first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gatewaymagnetapp.settings')

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import notifications.routing
import accounts.routing  # OK now because Django settings are configured

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns
            + accounts.routing.websocket_urlpatterns
        )
    ),
})







