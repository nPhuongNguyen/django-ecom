import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from ecom.chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

application = ProtocolTypeRouter({
    # HTTP (Django bình thường)
    "http": get_asgi_application(),

    # WebSocket
    "websocket": URLRouter([
        path("ws/chat/", ChatConsumer.as_asgi()),
    ]),
})