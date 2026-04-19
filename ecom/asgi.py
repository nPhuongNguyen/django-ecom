import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    # HTTP
    "http": ASGIStaticFilesHandler(django_asgi_app),

    # WebSocket
    # "websocket": URLRouter([
    #     path("ws/chat/", ChatConsumer.as_asgi()),
    # ]),
})