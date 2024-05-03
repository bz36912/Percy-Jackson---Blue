import numpy as np
import tensorflow as tf
import matplotlib as plt

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
    x_train = read_data("./data/walk.npy")
    labels = []
    for i in range(NUM_OF_SAMPLES):
        label = WALKING_ENCODE
        labels.append(label)
    labels = np.asarray(labels)
    y_train = labels
    print(np.shape(x_train))
    print(np.shape(y_train))
    input_shape = DATA_POINTS_PER_SAMPLE * NO_DATA_PER_POINT
    x_train = x_train.reshape(x_train.shape[0], input_shape)
    print("Input Data Shape: ", x_train.shape)
    x_train = x_train.astype('float32')
    y_train = y_train.astype('float32')
    
    

    