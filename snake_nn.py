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
top_fits = total_models // 10

# Game configurations
WIDTH = 480
HEIGHT = 480
GRID_D = 12
BLOCK_W = WIDTH / GRID_D
BLOCK_H = HEIGHT / GRID_D
MAX_MOVES = 100

# Save models to file
def save_pool():
    for i in range(total_models):
        current_pool[i].save_weights("Saved_Models/model" + str(i) + "_gen_" + str(generation) + ".keras")
    print("Pool saved")


def create_model():
    # create keras model
    model = Sequential()
    model.add(Dense(12, input_dim = 8, activation = 'relu'))
    model.add(Dense(15, activation = 'relu'))
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
    Produce offspring based on the best parrents
    May change how this works later
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
            if (random.uniform(0, 1) > .5):
                change = random.randint(-1,1)
                weights[i][j] += change
    
    return weights

def genetic_updates():
    print("I am a work in progress")

    global current_pool
    global fitness
    global generation
    new_weights = []
    total_fitness = 0

    # Calculate fitness
    for i in range(total_models):
        total_fitness += fitness[i]
    
    # Scaling fitness values
    '''
    for i in range(total_models):
        fitness[i] /= total_fitness
        if i > 0:
            fitness[i] += fitness[i - 1]
    '''

    parent_1 = random.randint(0, total_models - 1)
    parent_2 = random.randint(0, total_models - 1)
    index_1 = -1
    index_2 = -1

    for i in range(total_models):
        if fitness[i] >= fitness[parent_1]:
            index_1 = i

    for i in range(total_models):
        if fitness[i] >= fitness[parent_2]:
            if i != parent_1:
                index_2 = i

    top_models = np.argpartition(np.asarray(fitness), -int(top_fits))[-int(top_fits):]
    print(top_models)
    for i in range(5):
        print(fitness[top_models[i]])
    
    # Breeding time
    for i in range(total_models // 2):

        # Randomly choose from top ten percent
        id1 = top_models[random.randint(0, 4)]
        id2 = top_models[random.randint(0, 4)]
        if id2 == id1:
            id2 = top_models[random.randint(0, 4)]
        
        # new = model_crossover(index_1, index_2)
        new = model_crossover(id1, id2)
        update_w1 = model_mutate(new[0])
        update_w2 = model_mutate(new[1])
        new_weights.append(update_w1)
        new_weights.append(update_w2)

    # Reset fitness
    for i in range(len(new_weights)):
        fitness[i] = -100
        current_pool[i].set_weights(new_weights[i])

    # Save models (ADD ME LATER)
    generation += 1
    return

def check_if_closer(snake, fruit):
    head = snake.position[0]
    prev = snake.position[1]

    head_dis = math.sqrt((fruit.pos[0] - head[0]) ** 2 + (fruit.pos[1] - head[1]) ** 2)
    prev_dis = math.sqrt((fruit.pos[0] - prev[0]) ** 2 + (fruit.pos[1] - prev[1]) ** 2)

    if head_dis > prev_dis:
        return False
    return True

print("I am a work in progress")

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
        save_pool()
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
                # Adjust fitness
                # fitness[i] -= 10
                print(fitness[i])
                break

        # Clean up and print score
        # self.on_cleanup()
        # print(int(self.snake.score))
 
if __name__ == "__main__" :
    # Init models
    for i in range(total_models):
        model = create_model()
        current_pool.append(model)
        fitness.append(-100)

theApp = App()
while True:
    for i in range(total_models):
        fitness[i] = 0

    for i in range(total_models):    
        theApp.on_execute(i)
    print(fitness)
    genetic_updates()