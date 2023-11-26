from channels.consumer import database_sync_to_async
from .Snakeo.server import Snakeo
from channels.layers import get_channel_layer
import asyncio

class LobbyIdAlreadyExist(Exception):
    "Raised when attempt to create lobby with existing id"
    pass

class LobbyDoesNotExistError(Exception):
    "Raised when attempt to get lobby that not exist"
    pass


class Player():
    pass



    ### DO i even need that?


class Lobby():

    def __init__(self, id, owner, max_players):

        self.id = id
        self.max_players = max_players
        self.owner = owner
        self.status = "queue"
        self.server : Snakeo
        self.players = {}   ## MAYBE IT SHOULD BE DICT player - snake or another class  PLAYer?

        self._channel_layer = get_channel_layer()
        ## TEMPORARY 
        self.server = Snakeo()

   # do i need decor here??  
    def get_lobby_owner(self):
        return self.owner


    def create_server(self):
        self.server = Snakeo()

    async def start_game(self):

        self.server.init_gamefield()
        self.set_status("running")
        while True:   ## TODO w
            print('tick')
            data =  await self.server.gameloop()

            await self._channel_layer.group_send(self.id, {"type": "gameloop_data","data": data})    ## Я ПОхоже сдеклал что-то не так, больно страшный код получается


    def recive_direction(self, player, direction):
        print(self.players)
        self.players[player].recive_direction(direction)



    def set_status(self,status) -> None:    ### NOt complited TOdo Prorectin

        self.status = status
    
    def add_player(self, player):
        print('here', player not in self.players)
        #if player in self.players:  ### TODO it works user are same
            
        if self.status == "queue" and player not in self.players:
            
                self.players[player] = self.server.add_snake(str(player))
                print('added player,',player)

            

         


    def remove_player(self,player):  # TODO
        pass

class SnakeoLobbyManager(): 

    def __init__(self):
        self.snakeo_lobby = []

    def create_snakeo_lobby(self, id, owner, max_players=12):


    ####  Любой пользователь м ожет создать только одно лобби
        todel = [] 
        for lobby in self.snakeo_lobby:
            if lobby.owner == owner:
                if lobby.status != "running":
                    todel.append(lobby)

        for lobby_to_delete in todel:
            self.snakeo_lobby.remove(lobby_to_delete)

        ###### Это реализация удаления лобби, да выглядит кривовато

        try:
            for lobby in self.snakeo_lobby:
                if lobby.id == id:  
                    raise LobbyIdAlreadyExist
            
            new_lobby = Lobby(id=id, owner=owner, max_players=max_players)
            self.snakeo_lobby.append(new_lobby)
            print(self.snakeo_lobby)
        except  LobbyIdAlreadyExist:
            print("Lobby with that id already exist")
            print("Exception occured: ", LobbyIdAlreadyExist)  
    
    async def lobby_start_game(self, lobby_id, user): ### Нужно перенести функционал в класс лобби

        lobby = self.get_snakeo_lobby(lobby_id)
        if lobby:
            if lobby.owner != user or lobby.status == "running": ## TODO look bad
                return 0
        
            asyncio.create_task(lobby.start_game())
        else:
            print("TODOMEMEMEM       FAILED TO START LOBBY")

    # def delete_server(self, server_id):
        
    def add_player(self, lobby_id, player):
        lobby = self.get_snakeo_lobby(lobby_id)
        if lobby:
            return lobby.add_player(player)
        else:
            print("TODO       failed to add player, lobby does not exist")



    def get_snakeo_lobby(self, id):
        ## TODO PROTECTION
        try:
            for lobby in self.snakeo_lobby:
                if lobby.id == id:
                    return lobby
            raise LobbyDoesNotExistError
        except LobbyDoesNotExistError:
            print(f"Lobby with id - {id} does not exist")




snakeo_lobby_manager = SnakeoLobbyManager()




