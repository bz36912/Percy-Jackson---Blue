""" 
 ML.py files written by Bolong (Jack) Zhang and Daniel Barone
 This file is used to open the data that was collected and train the model on that data
 Currently there are two different models implemented in the file: temporal convolution and lstm
 This file can be modified to accomodate different types of data, and different types of activities by changing the following:
    - To change the activity types, modify the encoded values of the activities as well as modifying htme in the approapriate positions in y1
    - To change the types of data modify the NUM_OF_SAMPLES, DATA_POINTS_PER_SAMPLE and NO_DATA_PER_POINT variables
Running this program will display both a loss curve and a confusion matrix of the trained model.
Additionally, it will also save the model to the file path indicated in the model1.save() function
"""



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
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# Variables the keep track of how the data was collected
NUM_OF_SAMPLES = 50 # This is the number of samples that is in a given file
DATA_POINTS_PER_SAMPLE = 120 # This is the number of data points in each sample
NO_DATA_PER_POINT = 3 # This is teh number of dimension to each data point, it is 3 for x, y, z acceleration

# The encoded values of each of the activities being learned
WALKING_ENCODE = 1
RUNNING_ENCODE = 2
SITTING_ENCODE = 3
STANDING_ENCODE = 0
DO_NOTHING_ENCODE = 4

# Function that reads data from the given filepath and always returns a numpy array
def read_data(filepath) -> np.ndarray:
    data = np.load(filepath)
    return data

# Function that draws a confusion matrix on the model given by the user
def draw_confusion_matrix(model, to_predict, to_compare):
    predictions = model.predict(to_predict)
    predictions = np.argmax(predictions, axis=1)
    y_test_pred = np.argmax(to_compare, axis=0)
    cm = confusion_matrix(to_compare, predictions)
    cm_disp = ConfusionMatrixDisplay(confusion_matrix= cm)
    cm_disp.plot()
    plt.show()
    # classification_report(to_compare, predictions)

# Grapths the loss curve of the evaluated model
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

# One of the 2 potential models used, which is temporal convolution
def temporal_convolution_model(): # 6,693 params
    model1 = Sequential()
    model1.add(InputLayer((DATA_POINTS_PER_SAMPLE, NO_DATA_PER_POINT)))
    model1.add(Conv1D(32, 3, activation='relu', dilation_rate=1))
    model1.add(Conv1D(32, 3, activation='relu', dilation_rate=3))
    model1.add(Conv1D(32, 3, activation='relu', dilation_rate=9))
    # model1.add(Conv1D(32, 3, activation='relu', dilation_rate=8))
    # model1.add(Conv1D(5, 3, activation='relu', dilation_rate=1))
    model1.add(GlobalMaxPool1D())
    model1.add(Dense(5))
    model1.add(Softmax())

    model1.summary()
    return model1

def lstm_model():
    model1 = Sequential()
    model1.add(InputLayer((DATA_POINTS_PER_SAMPLE, NO_DATA_PER_POINT))) # type: ignore
    model1.add(LSTM(64)) # type: ignore
    model1.add(Dense(8, 'relu')) # type: ignore
    model1.add(Dense(5, 'softmax')) # type: ignore

    model1.summary()
    return model1

if __name__ == "__main__":
    # The following lines of code reads from the specified files and concatenates the values to x1
    # THen it concatenates the appropriate number of labels to y1
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
    temp = read_data("./data/do_nothing_while_sitting.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), DO_NOTHING_ENCODE)))
    temp = read_data("./data/do_nothing_while_standing.npy")
    x1 = np.concatenate((x1, temp))
    y1 = np.concatenate((y1, np.full((temp.shape[0],), DO_NOTHING_ENCODE)))
    
    print(np.shape(x1))
    print(np.shape(y1))

    # shuffle the data
    shuffled_idx = np.random.permutation(y1.size)
    y1 = np.copy(y1)[shuffled_idx]
    x1 = np.copy(x1)[shuffled_idx]

    # SPecify the training data and the validation data
    trainIndex = int(x1.shape[0] * 0.8)
    x_train, y_train = x1[:trainIndex], y1[:trainIndex]
    x_val, y_val = x1[trainIndex:], y1[trainIndex:]

    model1 = temporal_convolution_model()

    cp1 = ModelCheckpoint('model1/model1.keras', save_best_only=True)
    model1.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.0001), metrics=['sparse_categorical_accuracy'])

    hist = model1.fit(x_train, y_train, epochs=200, callbacks=[cp1], validation_data=(x_val, y_val), shuffle=True)
    loss_curve(hist.history)

    
    model1.evaluate(x=x_val, y=y_val)
    draw_confusion_matrix(model1, x_train, y_train)

    model1.save('model1/activity_classification_model_CNN_expanded.keras')
    print("end")