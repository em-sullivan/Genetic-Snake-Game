import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D, Activation


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