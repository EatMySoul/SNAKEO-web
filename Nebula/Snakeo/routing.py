from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import path, re_path
from django.core.asgi import get_asgi_application
from . import consumers

application = ProtocolTypeRouter({
    "http" : get_asgi_application(),
    # Django's ASGI application to handle traditional HTTP requests
    # WebSocket chat handler
    "websocket":
        URLRouter([
            re_path(r"ws/asgi/(?P<lobby_id>\w+)/$", consumers.GameLobby.as_asgi()),
        ])
})
