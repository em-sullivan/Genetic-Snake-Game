import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation

total_models = 1
current_pool = []

def save_pool():
    for i in range(total_models):
        current_pool[i].save_weights("Saved_Models/model" + str(i) + ".keras")
    print("Pool saved")


def create_model():
    # [TODO]
    # create keras model
    model = tf.keras.Sequential()
    model.add(Dense(3, input_shape=(3,)))
    model.add(Activation('relu'))
    model.add(Dense(7, input_shape=(3,)))
    model.add(Activation('relu'))
    model.add(Dense(1, input_shape=(3,)))
    model.add(Activation('sigmoid'))

    model.compile(loss='mse',optimizer='adam')

    return model