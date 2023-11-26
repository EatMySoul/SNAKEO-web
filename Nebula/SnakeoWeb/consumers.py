from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

from django.db.models.fields.related_descriptors import sync_to_async
from .snakeo_lobby_manager import snakeo_lobby_manager
from .models import Lobby
from channels.db import database_sync_to_async

class GameLobby(AsyncWebsocketConsumer):     ## SAME AS VIEW
 
    
    async def connect(self):

        print("ATTEMP TO CONNECT") ### Тут поблема, что при перезагрузке возникает новый консюмер как решать???
        self.lobby_id = self.scope["url_route"]["kwargs"]["lobby_id"]
        self.user = self.scope["user"]
    
        self.snakeo_lobby = snakeo_lobby_manager.get_snakeo_lobby(self.lobby_id)

        if not self.snakeo_lobby:  ## # IF lobby exist but server is not created abort connection
            return 0

        if self.snakeo_lobby.status == "queue":      ## TODO add get functions

            self.snakeo_lobby.add_player(self.user)

        
        if self.user in self.snakeo_lobby.players:
            await self.channel_layer.group_add(self.lobby_id, self.channel_name)

            print(self.snakeo_lobby.status)  
            await self.accept()            
 


    # Receive network data from snakeo server
    async def gameloop_data(self, event):

        data = event["data"] 
        await self.send(text_data=json.dumps(data))



    # Receive data from WebSocket
    async def receive(self, text_data):
 
        text_data_json = json.loads(text_data)
        direction = text_data_json["direction"]
        self.snakeo_lobby.recive_direction(self.user ,direction)



    
    async def get_init_network_data(self) -> dict:
        data = {}
        return data


    async def add_snake(self):   ### check if player in lobby if not add if lobby in running return error
        pass
        ## test
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.lobby_id, self.channel_name)

    
    
 

