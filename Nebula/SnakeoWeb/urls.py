from django.urls import path, re_path
from django.views.generic import  TemplateView
from . import views
from .consumers import GameLobby

urlpatterns = [
    path("main/", views.main_page, name="main_page"),
    re_path(r"lobby/(?P<lobby_id>\w+)/$", views.snakeo_lobby, name="snakeo_lobby"),
    path("react/", TemplateView.as_view(template_name = 'index.html' )),
]
