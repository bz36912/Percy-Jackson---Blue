import time
import tensorflow as tf
from tensorflow import keras
import numpy as np

data = np.load('data/stand3.npy')
data = data.reshape((-1, 120, 3))
activity_classifier = tf.keras.models.load_model('model1/activity_classification_model.keras')

for i in range(len(data)):
    temp = data[i].reshape((1,120,3))
    pred = activity_classifier.predict(temp)
    predictedClass = np.argmax(pred)
    print(pred, "predicited class is", predictedClass)