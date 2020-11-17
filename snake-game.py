'''
Simple snake game
'''
import sys
import pygame
from pygame.locals import *

# Game configurations
WIDTH = 480
HEIGHT = 480
GRID_D = 20
BLOCK_W = WIDTH / GRID_D
BLOCK_H = HEIGHT / GRID_D


class Snake:
    '''
    Player class
    '''
    def __init__(self):
        self.x, self.y = [], []
        self.x.append(WIDTH/2)
        self.y.append(HEIGHT/2)

        self.speed = BLOCK_W
        self.length = 6
        self.direction = 0
        self.color = (0, 255, 255)

        # For testing movement
        for i in range(0, self.length - 1):
            print(self.x[i])
            self.x.append(self.x[i] - BLOCK_W)
            self.y.append(HEIGHT/2)

    def update(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 0:
            self.x[0] = self.x[0] + self.speed
        elif self.direction == 1:
            self.x[0] = self.x[0] - self.speed
        elif self.direction == 2:
            self.y[0] = self.y[0] - self.speed
        elif self.direction == 3:
            self.y[0] = self.y[0] + self.speed

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1
    
    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface):
        for i in range(0, self.length):
            block = pygame.Rect((self.x[i], self.y[i]), (BLOCK_W, BLOCK_H))
            pygame.draw.rect(surface, self.color, block)




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
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.clock = pygame.time.Clock()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((0,124,0))
        
        # Fill every other space to create a multi color grid
        for i in range(0, int(GRID_D)):
            for j in range(0, int(GRID_D)):
                if (i + j) % 2 == 0:
                    block = pygame.Rect(((j * BLOCK_W, i * BLOCK_H), (BLOCK_W, BLOCK_H)))
                    pygame.draw.rect(self._display_surf, (0, 200, 0), block)

        self.snake.draw(self._display_surf)
        pygame.display.update()
        pass
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while (self._running):
            
            pygame.event.pump()
            key = pygame.key.get_pressed()

            if key[K_RIGHT]:
                self.snake.move_right()
            elif key[K_LEFT]:
                self.snake.move_left()
            elif key[K_UP]:
                self.snake.move_up()
            elif key[K_DOWN]:
                self.snake.move_down()
            
            self.snake.update()
            for event in pygame.event.get():
                self.on_event(event)

            print(self.snake.x, self.snake.y)
            self.on_loop()
            self.on_render()
            self.clock.tick(10)

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()