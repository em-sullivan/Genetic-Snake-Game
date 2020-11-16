'''
Simple snake game
'''
import sys
import pygame
from pygame.locals import *


WIDTH = 600
HEIGHT = 400

class Snake:
    '''
    Player class
    '''
    def __init__(self):
        self.x, self.y = 0,0
        self.speed = 0.5
        self.length = 1
        self.color = (0, 255, 255)

    def move_right(self):
        self.x = self.x + self.speed

    def move_left(self):
        self.x = self.x - self.speed
    
    def move_up(self):
        self.y = self.y - self.speed

    def move_down(self):
        self.y = self.y + self.speed

    def draw(self, surface):
        block = pygame.Rect((self.x, self.y), (20, 20))
        pygame.draw.rect(surface, self.color, block)


class App:
    '''
    Main App for game
    '''
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.snake = Snake()
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.snake.draw(self._display_surf)
        pygame.display.update()
        pass
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            
            pygame.event.pump()
            key = pygame.key.get_pressed()

            if key[K_RIGHT]:
                if (self.snake.x < self.width - 20):
                    self.snake.move_right()
            elif key[K_LEFT]:
                if (self.snake.x > 0):
                    self.snake.move_left()
            elif key[K_UP]:
                if (self.snake.y > 0):
                    self.snake.move_up()
            elif key[K_DOWN]:
                if (self.snake.y < self.height - 20):
                    self.snake.move_down()
            
            for event in pygame.event.get():
                self.on_event(event)

            print(self.snake.x)
            self.on_loop()
            self.on_render()

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()