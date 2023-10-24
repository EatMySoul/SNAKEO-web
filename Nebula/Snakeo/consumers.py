from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging


class GameLobby(AsyncWebsocketConsumer):     ## SAME AS VIEW

    
    async def connect(self):

        self.lobby_id = self.scope["url_route"]["kwargs"]["lobby_id"]

        await self.channel_layer.group_add(self.lobby_id, self.channel_name)
        print(self.channel_layer.groups)

        await self.accept()
        text_data = await self.get_init_network_data()

        await self.send(text_data=json.dumps({"test" : "123"}))  

        
    
    async def receive(self, text_data):
 
        text_data = json.loads(text_data)
        print(text_data)
        print(text_data["message"])

    
    async def get_init_network_data(self) -> dict:
        data = {}
        return data
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.lobby_name, self.channel_name)
    
    
 

