'''
main.py written by Bolong (Jack) Zhang and Daniel Barone
This is the main file where all functionality of all files are compartmentalised
Important aspects that might require changing in this file are:
    - The uart ports in the try/except loops 
    - The model that is loaded with tf.keras.models.load_model()
Additionally, users can modify the cutoff value specified is the line "if pred[0, predictedClass] > 0.5:"
as depending on the model, changing that value can make the overall predicitions more accurate.
'''

import tkinter as tk
from gui import GUI
from uart import Uart
import time
import tensorflow as tf
from tensorflow import keras
import threading
from ML_predict import UART_polling_thread_entry, MLInputQueue
import numpy as np
from mqtt import mqtt_thread_start, mqttTxDataQueue

root = tk.Tk()
gui = GUI(root)



if __name__ == "__main__":
    try:
        uart = Uart('COM7') # Change depending on the system running the program
    except:
        try:
            uart = Uart('/dev/tty.usbmodem0010502493171')
        except:
            uart = Uart('COM15')
    
    startTime = time.time() # Gets the start time of the program
    t = startTime
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model_CNN_expanded.keras') # Loads the specified model

    uartThread = threading.Thread(target=UART_polling_thread_entry, args=(uart,)) # Initialises the uart thread
    uartThread.start() # Starts the uart thread
    mqtt_thread_start() # Starts the mqtt thread
    gui.update() # Updates the gui, is done here to start the gui
    while True:        
        MLInput = MLInputQueue.get(block=True) 
        pred = activity_classifier.predict(MLInput)
        predictedClass = np.argmax(pred) # GIves the highest probability class of the predicted classes
        if pred[0, predictedClass] > 0.5: # If the probability is above 50% then it is considered valid and is displayed
            print(pred, "predicted class is", predictedClass)
            if predictedClass != 4:
                gui.change_images(predictedClass) # Changes the images depending on the predicted class
                gui.output_text_message(str(np.max(pred))) # Outputs the probability to the output box
                mqttTxDataQueue.put(predictedClass) # Puts the predicted class in the queue to be sent with MQTT
                gui.update() # Updates the gui
        else:
            print("prediction is UNCERTAIN class", predictedClass, pred[0, predictedClass])
        
        