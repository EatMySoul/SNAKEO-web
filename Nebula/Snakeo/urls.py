from django.urls import path
from django.views.generic import  TemplateView
from . import views
from .consumers import GameLobby

websocket_urlpatterns = [
    path("snakeo/react/", GameLobby.as_asgi())
]

urlpatterns = [
    path("index/", views.index, name="index"),
    path("react/", TemplateView.as_view(template_name = 'index.html' )),
    path("todelete/", views.index , name="index"),
]
