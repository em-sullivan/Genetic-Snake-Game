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

    def reset(self):
        self.position = []
        self.position.append([WIDTH/2, HEIGHT/2])
        self.length = 3
        self.direction = 0
        self.score = 0
        self.alive = True

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
      
    def collision(self, head):
        # Checks if snake hit boarder
        '''
        if self.position[0][0] < 0 or self.position[0][0] > WIDTH - BLOCK_W:
            return False
        if self.position[0][1] < 0 or self.position[0][1] > HEIGHT - BLOCK_H:
            return False

        # Checks if snake hit itself
        if self.position.count(self.position[0]) > 1:
            return False
        '''
        if head[0] < 0 or head[0] > WIDTH - BLOCK_W:
            return False
        if head[1] < 0 or head[1] > WIDTH - BLOCK_H:
            return False

        if self.position.count(head) > 1:
            return False

        # Return true is snake is didn't collide
        return True
       
    def check_head(self):
        '''
        Returns a numpy array if head will
        collide and die
        '''

        hit = np.array([0, 0, 0, 0])
        head_x = self.position[0][0]
        head_y = self.position[0][1]

        '''
        if self.direction == 0:
            hit[0] = self.collision([head_x + self.speed, head_y])
            hit[1] = self.collision([head_x, head_y - self.speed])
            hit[2] = self.collision([head_x, head_y + self.speed])

        if self.direction == 1:
            hit[0] = self.collision([head_x - self.speed, head_y])
            hit[1] = self.collision([head_x, head_y - self.speed])
            hit[2] = self.collision([head_x, head_y + self.speed])

        if self.direction == 2:
            hit[0] = self.collision([head_x, head_y - self.speed])
            hit[1] = self.collision([head_x + self.speed, head_y])
            hit[2] = self.collision([head_x - self.speed, head_y])

        if self.direction == 3:
            hit[0] = self.collision([head_x, head_y + self.speed])
            hit[1] = self.collision([head_x + self.speed, head_y])
            hit[2] = self.collision([head_x - self.speed, head_y])
        '''
        hit[0] = self.collision([head_x + self.speed,head_y])
        hit[1] = self.collision([head_x - self.speed, head_y])
        hit[2] = self.collision([head_x, head_y - self.speed])
        hit[3] = self.collision([head_x, head_y + self.speed])

        return 1 - hit


    def check_fruit(self, fruit):
        hit = np.array([0, 0, 0, 0])
        head_x = self.position[0][0]
        head_y = self.position[0][1]

        if ([head_x + self.speed, head_y] == fruit.pos):
            hit[0] = 1
        if ([head_x - self.speed, head_y] == fruit.pos):
            hit[1] = 1
        if ([head_x, head_y - self.speed] == fruit.pos):
            hit[2] = 1
        if ([head_x, head_y + self.speed] == fruit.pos):
            hit[3] = 1
        
        return hit
    
    def eat(self, fruit):
        
        # Checks if head is going to eat fruit
        x = self.position[0][0]
        y = self.position[0][1]
        
        # Figures out where head would be next movemnet
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
    
    def position(self):
        return self.pos


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
        self.pause = False
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()
 
    def on_event(self, event):

        # Quit game
        if event.type == pygame.QUIT:
            self._running = False
        
        # Change direction of snake
        if event.type == pygame.KEYDOWN:
            if event.key == K_RIGHT:
                if self.snake.direction != 1:
                    self.snake.move_right()
            elif event.key == K_LEFT:
                if self.snake.direction != 0:
                    self.snake.move_left()
            elif event.key == K_UP:
                if self.snake.direction != 3:
                    self.snake.move_up()
            elif event.key == K_DOWN:
                if self.snake.direction != 2:
                    self.snake.move_down()
            elif event.key == K_p:
                self.pause = not self.pause

    
    def on_loop(self):
        self.snake.alive = self.snake.collision(self.snake.position[0])
        if self.snake.alive is False:
            return
        self.snake.eat(self.fruit)
        self.snake.update()
        #print(self.snake.check_head())
        #print(self.snake.check_fruit(self.fruit))
    
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
        
            for event in pygame.event.get():
                self.on_event(event)

            # Checks if game is paused
            if self.pause is False:
                self.on_loop()
                self.on_render()
                self.clock.tick(11)

            # Reset when snake dies
            if self.snake.alive == False:
                print(int(self.snake.score))
                self.snake.reset()
                self.fruit.random_generate()

        # Clean up and print score
        self.on_cleanup()
        print(int(self.snake.score))
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()