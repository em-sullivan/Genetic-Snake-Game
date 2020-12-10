import random
import sys
import math
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation

from snake_game import Snake
from snake_game import Fruit
import pygame
from pygame.locals import *

# Neural Network globals
total_models = 50
current_pool = []
fitness = []
generation = 1
top_fits = total_models // 5

# 1 if want to save pool, 0 if not
save = 0
save_location = "Saved_Models/model"
load = 0
load_location = "Saved_Models-ok/model"

# Game configurations
WIDTH = 480
HEIGHT = 480
GRID_D = 12
BLOCK_W = WIDTH / GRID_D
BLOCK_H = HEIGHT / GRID_D
MAX_MOVES = 100
score = []

# Save models to file
def save_pool():
    for i in range(total_models):
        current_pool[i].save_weights(save_location + str(i) + ".keras")
    print("Pool saved")


def create_model():
    '''
    Create Neural Network as a keras model
    '''
    model = Sequential()
    model.add(Dense(12, input_dim = 8, activation = 'relu'))
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(4, activation = 'sigmoid'))
    model.compile(loss='mse', optimizer='adam')

    return model

def predict_direction(snake, fruit, model_num):
    '''
    This function feeds information into the model, then determines
    which direction the snake should go
    '''
    direction = snake.check_head()
    fruit = snake.check_fruit(fruit)

    n_input = np.concatenate([direction, fruit])
    n_input = np.atleast_2d(n_input)

    output = current_pool[model_num].predict(n_input, 1)
 
    return output.argmax()

def model_crossover(parent_1, parent_2):
    '''
    Produce offspring based on the best parents
    '''
    global current_pool

    # Weight of parents
    weight1 = current_pool[parent_1].get_weights()
    weight2 = current_pool[parent_2].get_weights()
    new_weight1 = weight1
    new_weight2 = weight2

    # Gene
    gene = random.randint(0, len(new_weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]
    return np.asarray([new_weight1, new_weight2])

def model_mutate(weights):
    '''
    Mutate the weights of a model
    '''
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if (random.uniform(0, 1) > .7):
                change = random.uniform(-.5,.5)
                weights[i][j] += change
    
    return weights

def genetic_updates():
    print("I am a work in progress")

    global current_pool
    global fitness
    global generation
    new_weights = []

    # Calculate total fitness
    total_fitness = sum(fitness)
    
    # Crossover_time
    for i in range(total_models // 2):
        choice_1 = random.randint(0, total_fitness)
        choice_2 = random.randint(0, total_fitness)
        parent_1 = -1
        parent_2 = -1

        # Pick 1st parent
        current = 0
        for idx in range(total_models):
            current += fitness[idx]
            if current >= choice_1:
                parent_1 = idx
                break
        
        # Pick 2nd parent
        current = 0
        for idx in range(total_models):
            current += fitness[idx]
            if current >= choice_2:
                parent_2 = idx
                break
  
        # Model crossover between two parents
        new = model_crossover(parent_1, parent_2)
        
        # Mutate models
        update_w1 = model_mutate(new[0])
        update_w2 = model_mutate(new[1])
        new_weights.append(update_w1)
        new_weights.append(update_w2)

    # Set new weights, reset fitness
    for i in range(len(new_weights)):
        fitness[i] = -100
        current_pool[i].set_weights(new_weights[i])

    generation += 1
    return

def check_if_closer(snake, fruit):
    head = snake.position[0]
    prev = snake.position[1]

    # Calculate the heads distance from the fruit, and the previous spot
    # to see if it got closer
    head_dis = math.sqrt((fruit.pos[0] - head[0]) ** 2 + (fruit.pos[1] - head[1]) ** 2)
    prev_dis = math.sqrt((fruit.pos[0] - prev[0]) ** 2 + (fruit.pos[1] - prev[1]) ** 2)

    if head_dis > prev_dis:
        return False
    return True


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
        self.moves = 0
        self.frames = 11
 
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
            if event.key == K_UP:
                if self.frames < 1000000000:
                    self.frames *= 10
            elif event.key == K_DOWN:
                if self.frames > 10:
                    self.frames /= 10
            elif event.key == K_p:
                self.pause = not self.pause
            elif event.key == K_q:
                self.on_cleanup()

    
    def on_loop(self, model_num):
        self.snake.alive = self.snake.collision(self.snake.position[0])
        if self.snake.alive is False:
            return
        if self.snake.eat(self.fruit) is True:
            fitness[model_num] += 150
            score[model_num] += 1
            self.moves = 0
        self.snake.update()
        
        if check_if_closer(self.snake, self.fruit):
            fitness[model_num] += 10
        else:
            fitness[model_num] -= 0

        self.moves += 1
    
    def on_render(self, model_num):
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
        pygame.display.set_caption("Gen: " + str(generation) + " Model: " + str(model_num) + " Score: " + str(self.snake.score) + " Tick " + str(self.frames))
        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()
        sys.exit()
 
    def on_execute(self, i):
        if self.on_init() == False:
            self._running = False
 
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            
            self.snake.direction = predict_direction(self.snake, self.fruit, i)

            # Checks if game is paused
            if self.pause is False:
                self.on_loop(i)
                self.on_render(i)
                self.clock.tick(self.frames)

            # Reset when snake dies
            if self.snake.alive == False or self.moves == MAX_MOVES:
                print(int(self.snake.score))
                self.snake.reset()
                self.fruit.random_generate()
                self.moves = 0
               
                # Print fitness
                print(fitness[i])
                break

        # Clean up and print score
        # self.on_cleanup()
        print(int(self.snake.score))
 
if __name__ == "__main__" :
    # Init models
    for i in range(total_models):
        model = create_model()
        current_pool.append(model)
        fitness.append(-100)
        score.append(0)

    if load == 1:
        for i in range(total_models):
            current_pool[i].load_weights(load_location + str(i) + ".keras")

theApp = App()
while True:

    # Reset fitness scores and player scores
    for i in range(total_models):
        fitness[i] = 0
        score[i] = 0

    # Play game for each model
    for i in range(total_models):    
        theApp.on_execute(i)
    
    # Print high score to screen
    print("Higest score: " + str(max(score)) + " Model: " + str(score.index(max(score))) + " Gen: " + str(generation))
    
    # Write these values to a file
    #fi = open("results.txt", "a+")
    #fi.write("Higest score: " + str(max(score)) + " Model: " + str(score.index(max(score))) + " Gen: " + str(generation) + "\r\n")
    #fi.close()

    # Save pool
    if save == 1:
        save_pool()
    genetic_updates()