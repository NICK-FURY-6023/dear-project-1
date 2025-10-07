import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import ChatConsumer, EchoConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')

# Django ASGI application must be initialized before importing consumers
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),
            path('ws/chat/', EchoConsumer.as_asgi()),
        ])
    ),
})
