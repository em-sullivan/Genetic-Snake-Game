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
        temp = []
        for i in range(self.length-1, 0, -1):
            temp.insert(0, self.position[i - 1])
        

        # Update head position
        if self.direction == 0:
            #self.x[0] = self.x[0] + self.speed
            #self.position[0][0] += self.speed
            temp.insert(0, [self.position[0][0] + self.speed, self.position[0][1]])
        elif self.direction == 1:
            #self.x[0] = self.x[0] - self.speed
            #self.position[0][0] -= self.speed
            temp.insert(0, [self.position[0][0] - self.speed, self.position[0][1]])
        elif self.direction == 2:
            #self.y[0] = self.y[0] - self.speed
            #self.position[0][1] -= self.speed
            temp.insert(0, [self.position[0][0], self.position[0][1] - self.speed])
        elif self.direction == 3:
            #self.y[0] = self.y[0] + self.speed
            #self.position[0][1] += self.speed
            temp.insert(0, [self.position[0][0], self.position[0][1] + self.speed])
        
        self.position = temp
        
    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1
    
    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3
      
    def collision(self):
        # May change how this works later, checks if snake goes
        # out of bound
        x = self.position[0][0]
        y = self.position[0][1]
        if x < 0 or x > WIDTH - BLOCK_W:
            self.alive = False
        if y < 0 or y > HEIGHT - BLOCK_H:
            self.alive = False

        # Checks if snake hit itself
        if self.position.count(self.position[0]) > 1:
            self.alive = False
        #for i in range(1, self.length):
        #    if x == self.position[i][0]:
        #        if y == self.position[i][1]:
        #            self.alive = False

    def eat(self, fruit):
        x = self.position[0][0]
        y = self.position[0][1]
        if (x == fruit.pos[0] and y == fruit.pos[1]):
            self.position.append([fruit.pos[0], fruit.pos[1]])
            self.length = self.length + 1
            
            while True:
                fruit.random_generate()
                print("Fruit:", fruit.pos)
                print("Snake:", self.position)
                print(self.position.count(fruit.pos))
                if self.position.count(fruit.pos) == 0:
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
        self.snake.eat(self.fruit)
    
    def on_render(self):
        self._display_surf.fill((0,124,0))
        
        # Fill every other space to create a multi color grid
        for i in range(0, int(GRID_D)):
            for j in range(0, int(GRID_D)):
                if (i + j) % 2 == 0:
                    block = pygame.Rect(((j * BLOCK_W, i * BLOCK_H), (BLOCK_W, BLOCK_H)))
                    pygame.draw.rect(self._display_surf, (0, 200, 0), block)

        self.snake.draw(self._display_surf)
        self.fruit.draw(self._display_surf)
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
            self.snake.update()
            self.clock.tick(11)
            if self.snake.alive == False:
                break

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()