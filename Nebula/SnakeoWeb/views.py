from django.shortcuts import HttpResponseRedirect, render
from django.http import HttpResponse
from django.shortcuts import render

from .snakeo_lobby_manager import snakeo_lobby_manager
from .forms import LobbyCreationForm
import shortuuid
import asyncio

# Create your views here.

def main_page(request):
    if request.method == "POST":

        user = request.user
        print("in view ", user)

        form = LobbyCreationForm(request.POST)
        if form.is_valid():
            id = shortuuid.uuid()[:8]
            snakeo_lobby_manager.create_snakeo_lobby(id=id, owner=user)  
            return HttpResponseRedirect(f"/snakeo/lobby/{id}")
    else: 
        form = LobbyCreationForm()
    return render(request, "main_page.html", {"form": form})


async def snakeo_lobby(request, lobby_id):

    if request.method == "POST":
        await snakeo_lobby_manager.lobby_start_game(lobby_id, request.user)
    else:
        pass

    return render(request, "snakeo_lobby.html", {"lobby_id" : lobby_id})


        
