import random
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation

from snake_game import Snake
from snake_game import Fruit

total_models = 25
current_pool = []
fitness = []

# Save models to file
def save_pool():
    for i in range(total_models):
        current_pool[i].save_weights("Saved_Models/model" + str(i) + ".keras")
    print("Pool saved")


def create_model():
    # create keras model
    model = Sequential()
    model.add(Dense(12, input_dim = 8, activation = 'relu'))
    model.add(Dense(15, activation = 'relu'))
    model.add(Dense(4, activation = 'sigmoid'))
    model.compile(loss='mse',optimizer='adam')

    return model

def predict_direction(game, snake, fruit):
    '''
    This function feeds information into the model, then determines
    which direction the snake should go
    '''

    print("WORK ONE ME")

def model_crossover(parent_1, parent_2):
    '''
    Produce offspring based on the best parrents
    May change how this works later
    '''
    print("Work on ME")
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
    print("Work on ME")
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if (random.uniform(0, 1) > .5):
                change = random.randint(-1,1)
                weights[i][j] += change
    
    return weights


print("I am a work in progress")
# Init models
for i in range(total_models):
    model = create_model()
    current_pool.append(model)
    fitness.append(-100)
