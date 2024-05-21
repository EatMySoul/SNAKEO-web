from random import randint
import pickle
import asyncio
from enum import Enum

MAP_SIZE = 10
GAME_SPEED = 100
MAX_PLAYERS = 2
SCORE_TODO = 1
TICK_RATE = 1



class Snakeo:

    def __init__(self):

        self.snakes = []
        self.food_pos = []
        self.snakes_alive = 0
        self.game_status = "queue"

    def init_gamefield(self) -> None:
        self.snakes_alive = len(self.snakes)
        for _ in range(self.snakes_alive):
            self.add_food()




    
    def add_snake(self, name, body : list = [[0,0],
                                             [1,0],
                                             [2,0]]):
        snake = Snake(name,body)
        self.snakes.append(snake)
        return snake



    async def gameloop(self) -> dict:
        """starting gameloop of the game"""

        await asyncio.sleep(TICK_RATE)

        for snake in self.snakes:
            if snake.living:
                snake.direction = snake.next_direction
                snake.move()
        self.check_snakes_collision()
                
        data = self.get_network_data()

        return data


    def add_food(self) -> None:
        """add food to the game field"""

        x = randint(0, int(MAP_SIZE - 1))
        y = randint(0, int(MAP_SIZE - 1))

        snakes_coords = self.get_snake_coord()

        while [x, y] in snakes_coords:
            x = randint(0, int(MAP_SIZE - 1 ))
            y = randint(0, int(MAP_SIZE - 1 ))

        self.food_pos.append([x, y])




    def get_snake_coord(self,except_snake = None) -> list:
        """getting list of coordinates of each snake segment"""
        cordinates = []
        for snake in self.snakes:
            if snake.living:
                for segment in snake.body:
                    cordinates.append(segment)
        if except_snake:
            cordinates.remove(except_snake.body[0])
        return cordinates



    def check_snakes_collision(self) -> None:
        for snake in self.snakes:
            if snake.living:
                for food in self.food_pos:
                    if snake.body[0] == food:
                        snake.add_segment()
                        snake.score += SCORE_TODO
                        self.food_pos.remove(food)
                        self.add_food()
                if snake.body[0] in self.get_snake_coord(except_snake = snake):
                    snake.death()
                    self.snakes_alive -= 1

     ############################NETWORK################################           
    def get_init_network_data(self) -> list:
        """return init network data"""

        init_data = [self.food_pos]
        for snake in self.snakes:
            init_data.append({'name': snake.name,
                              'body': snake.body,
                              'score': snake.score,
                              'living': True})
        return init_data



    def get_network_data(self) -> dict:
        """return game's network data"""

        data = {"food" : self.food_pos,
                "snakes": [] }

        for snake in self.snakes:
            data["snakes"].append({
                'body': snake.body,
                'score': snake.score,
                'living': snake.living,
                'name': snake.name})

        return data





class Snake:

    
    def __init__(self, name : str, body : list):
        
        

        self.name : str = name 
        self.living : bool = True
        self.score : int = 0
        self.body : list =  body  # IS list of segments

        self.direction  = "up"
        self.next_direction  = "up"


    def move(self) -> None:
        """moveing snake in game field"""
        if self.living:
            for segment in range(len(self.body) - 1, 0, -1):
                self.body[segment][0] = self.body[segment - 1][0]
                self.body[segment][1] = self.body[segment - 1][1]
    
            if self.direction == "right":
                if self.body[0][1] == MAP_SIZE - 1:
                    self.body[0][1] = 0
                else:
                    self.body[0][1] += 1
    
            elif self.direction == "left":
                if self.body[0][1] == 0:
                    self.body[0][1] = MAP_SIZE - 1
                else:
                    self.body[0][1] -= 1
            elif self.direction == "up":
                if self.body[0][0] == 0:
                    self.body[0][0] = MAP_SIZE - 1
                else:
                    self.body[0][0] -= 1
            elif self.direction == "down":
                if self.body[0][0] == MAP_SIZE - 1:
                    self.body[0][0] = 0
                else:
                    self.body[0][0] += 1
    

    def recive_direction(self, direction : str) -> None: ## TODO remane change or set direction
        """recive players input"""
        """importtant to make this oneshoot in tick to prevent input bugs"""
        if self.living:
           if direction == 'left' and self.direction != 'right':
               self.next_direction = 'left'
           elif direction == 'right' and self.direction != 'left':
               self.next_direction = 'right'
           elif direction == 'up' and self.direction != 'down':
               self.next_direction = 'up'
           elif direction == 'down' and self.direction != 'up':
               self.next_direction = 'down'


    def add_segment(self) -> None:
        """add segment to the snake"""
        new_segment  = [self.body[-1][0],  self.body[-1][1]]
        self.body.append(new_segment)


    def death(self):
        """kill the snake"""
        self.living = False


def main():
    pass


if __name__ == "__main__":
    main()

