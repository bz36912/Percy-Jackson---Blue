import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
import matplotlib as plt
import pandas as pd
import os

# should i normalize the data

NUM_OF_SAMPLES = 50
DATA_POINTS_PER_SAMPLE = 120
NO_DATA_PER_POINT = 3
WALKING_ENCODE = 1
RUNNING_ENCODE = 2
SITTING_ENCODE = 3
STANDING_ENCODE = 4

def read_data(filepath):
    data = np.load(filepath)
    return data



if __name__ == "__main__":
    x1 = read_data("./data/walk.npy")
    labels = []
    for i in range(NUM_OF_SAMPLES):
        label = WALKING_ENCODE
        labels.append(label)
    labels = np.asarray(labels)
    y1 = labels
    print(np.shape(x1))
    print(np.shape(y1))
    input_shape = DATA_POINTS_PER_SAMPLE * NO_DATA_PER_POINT
    x1 = x1.reshape(x1.shape[0], input_shape, 1)
    y1 = y1.reshape(NUM_OF_SAMPLES, 1)
    print("Input Data Shape: ", x1.shape)
    print("y1 data shape: ", y1.shape)
    x1 = x1.astype('float32')
    y1 = y1.astype('float32')

    x_train, y_train = x1[:40], y1[:40]
    x_val, y_val = x1[40:50], y1[40:50]
    # x_test, y_test = x1[45:50], y1[45:50]

    
    model1 = Sequential()
    model1.add(InputLayer((input_shape,1)))
    model1.add(LSTM(64))
    model1.add(Dense(8, 'relu'))
    model1.add(Dense(1, 'linear'))

    model1.summary()

    """ model1 = Sequential()
    model1.add(LSTMV1(32, return_sequences=True, input_shape=(input_shape,1), activation='relu'))
    model1.add(LSTMV1(32,return_sequences=True, activation='relu'))
    model1.add(Reshape((1, input_shape, 32)))
    model1.add(Conv1D(filters=64,kernel_size=2, activation='relu', strides=2))
    model1.add(Reshape((180, 64)))
    model1.add(MaxPool1D(pool_size=4, padding='same'))
    model1.add(Conv1D(filters=192, kernel_size=2, activation='relu', strides=1))
    model1.add(Reshape((44, 192)))
    model1.add(GlobalAveragePooling1D())
    model1.add(BatchNormalization(epsilon=1e-06))
    model1.add(Dense(6))
    model1.add(Activation('softmax'))

    model1.summary() """

    cp1 = ModelCheckpoint('model1/model1.keras', save_best_only=True)
    model1.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[RootMeanSquaredError()])

    model1.fit(x_train, y_train, epochs=10, callbacks=[cp1])

    
    
    
    

    