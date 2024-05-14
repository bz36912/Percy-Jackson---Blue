import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import * # type: ignore
from tensorflow.keras.callbacks import ModelCheckpoint # type: ignore
from tensorflow.keras.losses import MeanSquaredError # type: ignore
from tensorflow.keras.metrics import RootMeanSquaredError # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
import matplotlib.pyplot as plt
import pandas as pd
import os


NUM_OF_SAMPLES = 50
DATA_POINTS_PER_SAMPLE = 120
NO_DATA_PER_POINT = 3
WALKING_ENCODE = 1
RUNNING_ENCODE = 2
SITTING_ENCODE = 3
STANDING_ENCODE = 0

def read_data(filepath) -> np.ndarray:
    data = np.load(filepath)
    return data

def loss_curve(epochStats):
    def plot_train_n_val(ax:plt.Axes, epochStats, metricName):
        ax.set_title(metricName)
        # training set
        x = np.arange(len(epochStats[metricName]))
        for metric in [metricName, "val_" + metricName]: # training set then validation set
            ax.plot(x, epochStats[metric], label=metric)
            coordinates = (x[-1], epochStats[metric][-1])
            text = str(round(epochStats[metric][-1], 4))
            ax.text(coordinates[0], coordinates[1], text, color='r')
        ax.legend()
        ax.set_xlabel("Epoch")
        ax.grid()

    # graph the losses and graph the accuracy in two subplots
    x = np.arange(len(epochStats['loss']))
    fig, ax = plt.subplots(2, 1)
    # ax[1].axhline(y=0.66, color='g', linestyle='--')
    ax[1].axhline(y=0.7, color='m', linestyle='--')
    plot_train_n_val(ax[0], epochStats, 'loss')
    plot_train_n_val(ax[1], epochStats, 'sparse_categorical_accuracy')
    ax[0].set_ylabel("Loss")
    ax[1].set_ylabel("Accuracy")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    x1 = read_data("./data/walk.npy")
    y1 = np.zeros((0,))
    y1 = np.concatenate((y1, np.full((x1.shape[0],), WALKING_ENCODE)))
    temp = read_data("./data/sit2.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), SITTING_ENCODE)))
    temp = read_data("./data/stand2.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), STANDING_ENCODE)))

    temp = read_data("./data/walk3.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), WALKING_ENCODE)))
    temp = read_data("./data/sit3.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), SITTING_ENCODE)))
    temp = read_data("./data/stand3.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), STANDING_ENCODE)))
    temp = read_data("./data/running2.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), RUNNING_ENCODE)))
    temp = read_data("./data/running3.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), RUNNING_ENCODE)))
    
    print(np.shape(x1))
    print(np.shape(y1))

    # shuffle the data
    shuffled_idx = np.random.permutation(y1.size)
    y1 = np.copy(y1)[shuffled_idx]
    x1 = np.copy(x1)[shuffled_idx]

    trainIndex = int(x1.shape[0] * 0.8)
    x_train, y_train = x1[:trainIndex], y1[:trainIndex]
    x_val, y_val = x1[trainIndex:], y1[trainIndex:]
    # x_test, y_test = x1[45:50], y1[45:50]

    
    model1 = Sequential()
    model1.add(InputLayer((DATA_POINTS_PER_SAMPLE, NO_DATA_PER_POINT))) # type: ignore
    model1.add(LSTM(64)) # type: ignore
    model1.add(Dense(8, 'relu')) # type: ignore
    model1.add(Dense(4, 'softmax')) # type: ignore

    model1.summary()

    cp1 = ModelCheckpoint('model1/model1.keras', save_best_only=True)
    model1.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.0001), metrics=['sparse_categorical_accuracy'])

    hist = model1.fit(x_train, y_train, epochs=200, callbacks=[cp1], validation_data=(x_val, y_val), shuffle=True)
    loss_curve(hist.history)
    model1.evaluate(x=x_val, y=y_val)
    model1.save('model1/activity_classification_model.keras')
    print("end")

    
    
    
    

    