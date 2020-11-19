'''
Simple snake game
'''
import random
import pygame
import numpy as np
from pygame.locals import *

# Game configurations
WIDTH = 480
HEIGHT = 480
GRID_D = 12
BLOCK_W = WIDTH / GRID_D
BLOCK_H = HEIGHT / GRID_D


class Snake:
    '''
    Player class
    '''
    def __init__(self):
        self.position = []
        self.position.append([WIDTH/2, HEIGHT/2])

        self.speed = BLOCK_W
        self.length = 3
        self.direction = 0
        self.color = (0, 255, 255)
        self.score = 0
        self.alive = True

        # For testing movement
        for i in range(0, self.length - 1):
            self.position.append([self.position[i][0] - BLOCK_W, HEIGHT/2])

    def update(self):

        # Update Snake body
        for i in range(self.length-1, 0, -1):
            self.position[i][0] = self.position[i-1][0]
            self.position[i][1] = self.position[i-1][1]    

        # Update head position
        if self.direction == 0:
            self.position[0][0] += self.speed

        elif self.direction == 1:
            self.position[0][0] -= self.speed

        elif self.direction == 2:
            self.position[0][1] -= self.speed

        elif self.direction == 3:
            self.position[0][1] += self.speed
        
    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1
    
    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3
      
    def collision(self):
        # Checks if snake hit boarder
        if self.position[0][0] < 0 or self.position[0][0] > WIDTH - BLOCK_W:
            self.alive = False
        if self.position[0][1] < 0 or self.position[0][1] > HEIGHT - BLOCK_H:
            self.alive = False

        # Checks if snake hit itself
        if self.position.count(self.position[0]) > 1:
            self.alive = False
       

    def eat(self, fruit):
        
        # Checks if head is going to eat fruit
        x = self.position[0][0]
        y = self.position[0][1]
        if (self.direction == 0):
            x += self.speed
        elif (self.direction == 1):
            x -= self.speed
        elif (self.direction == 2):
            y -= self.speed
        elif (self.direction == 3):
            y += self.speed

        # Extends body if fruit is eaten
        if (x == fruit.pos[0] and y == fruit.pos[1]):
            self.position.append([fruit.pos[0], fruit.pos[1]])
            self.length += 1
            self.score += 1
            
            # Randomly genereate new fruit on board, make sure it
            # is not on the snake body
            while True:
                fruit.random_generate()
                if fruit.pos not in self.position:
                    break

    def draw(self, surface):
        for i in range(0, self.length):
            block = pygame.Rect((self.position[i][0], self.position[i][1]), (BLOCK_W, BLOCK_H))
            pygame.draw.rect(surface, self.color, block)


class Fruit:
    '''
    Fruit for snake to eat
    '''
    def __init__(self):
        self.pos =[0, 0]
        self.color = (255, 0, 0)
        self.random_generate()

    def random_generate(self):
        self.pos[0] = random.randint(0, GRID_D - 1) * BLOCK_W
        self.pos[1] = random.randint(0, GRID_D - 1) * BLOCK_H

    def draw(self, surface):
        apple = pygame.Rect((self.pos[0], self.pos[1]), (BLOCK_W, BLOCK_H))
        pygame.draw.rect(surface, self.color, apple)


class App:
    '''
    Main App for game
    '''
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.clock = None
        self.snake = Snake()
        self.fruit = Fruit()
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        self.snake.collision()
        if self.snake.alive is False:
            return
        self.snake.eat(self.fruit)
        self.snake.update()
    
    def on_render(self):
        self._display_surf.fill((0,124,0))
        
        # Fill every other space to create a multi color grid
        for i in range(0, int(GRID_D)):
            for j in range(0, int(GRID_D)):
                if (i + j) % 2 == 0:
                    block = pygame.Rect(((j * BLOCK_W, i * BLOCK_H), (BLOCK_W, BLOCK_H)))
                    pygame.draw.rect(self._display_surf, (0, 200, 0), block)

        # Draw sanke and fruit
        self.fruit.draw(self._display_surf)
        self.snake.draw(self._display_surf)
        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while (self._running):
            
            pygame.event.pump()
            key = pygame.key.get_pressed()

            if key[K_RIGHT]:
                if self.snake.direction != 1:
                    self.snake.move_right()
            elif key[K_LEFT]:
                if self.snake.direction != 0:
                    self.snake.move_left()
            elif key[K_UP]:
                if self.snake.direction != 3:
                    self.snake.move_up()
            elif key[K_DOWN]:
                if self.snake.direction != 2:
                    self.snake.move_down()
                    
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            self.clock.tick(11)

            # Quite when snake dies
            if self.snake.alive == False:
                break

        # Clean up and print score
        self.on_cleanup()
        print(int(self.snake.score))
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()