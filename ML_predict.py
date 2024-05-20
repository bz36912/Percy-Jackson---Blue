'''
ML_predict.py written by Bolong (Jack) Zhang
This is the program that creates another thread of excecution for main.py, that takes acceleration values from the uart queue
and makes predictions
This files can be changed to run without the need of the main.py file, however doing so will lose access to the gui
Additionally, other users can change the nuber of overlapping data points between each prediction to see if the model becomes
more or less accurate.
'''

from data_log import get_uart_data, STEPS_PER_SAMPLE, NUM_FEATURES
from uart import Uart
from queue import Queue
import numpy as np
SIZE_OF_SUBSET = 31
import threading
import tensorflow as tf
import time


MLInputQueue = Queue() # The queue where the predicted classes would be passed into

# the entry for the thread for main.py
# the following function waits for 120 samples from the the uart buffer then uses those values to predict a class
# The next prediction will then use a number of samples from the previous samples, meaning each predicition will overlap with each other
# The number of overlapping data points is defined in the variable SIZE_OF_SUBSET
def UART_polling_thread_entry(uart:Uart):
    MLInput = np.zeros((1, STEPS_PER_SAMPLE, NUM_FEATURES), dtype=float)
    timeStep = STEPS_PER_SAMPLE - SIZE_OF_SUBSET
    uart.reset()
    while True:
        MLInput[0, timeStep, ::] = get_uart_data(uart)
        timeStep += 1
        if timeStep >= STEPS_PER_SAMPLE:
            MLInputQueue.put(MLInput)
            MLInput[0, :-SIZE_OF_SUBSET, ::] = MLInput[0, SIZE_OF_SUBSET:, ::]
            timeStep = STEPS_PER_SAMPLE - SIZE_OF_SUBSET
            uart.reset()

# The following code isn't needed if the program is being run from the main.py file
# However, if the gui is not needed, this code can be uncommented and the live predictions can be done from just this file
""" 
if __name__ == "__main__":
    print("start of ML_predict.py")
    try:
        uart = Uart('COM7') # Change depending on thing
    except:
        try:
            uart = Uart('/dev/tty.usbmodem0010502493171')
        except:
            uart = Uart('COM15')
    uartThread = threading.Thread(target=UART_polling_thread_entry, args=(uart,))
    uartThread.start()
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model_CNN_expanded.keras')

    prevTime = time.time()
    while True:
        # try:
        MLInput = MLInputQueue.get(block=True)
        # print("get ML input time", time.time() - prevTime)
        prevTime = time.time()
        # print("first timestep", MLInput[0, 0, ::])
        # print("last timestep", MLInput[0, -1, ::])

        pred = activity_classifier.predict(MLInput)
        # print("ML prediction time", time.time() - prevTime)
        prevTime = time.time()

        predictedClass = np.argmax(pred)
        if pred[0, predictedClass] > 0.7:
            print(f"class is {predictedClass}, prob: {pred[0, predictedClass]}")
        else:
            print(f"MAYBE class {predictedClass}, prob: {pred[0, predictedClass]}")
        # gui.update()
        # except:
            # pass # the MLInput is currently not ready
 """
