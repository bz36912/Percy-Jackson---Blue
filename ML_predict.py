from data_log import get_uart_data, STEPS_PER_SAMPLE, NUM_FEATURES
from uart import Uart
from queue import Queue
import numpy as np
SIZE_OF_SUBSET = 31
import threading
import tensorflow as tf
import time

MLInputQueue = Queue()
def UART_polling_thread_entry(uart:Uart):
    MLInput = np.zeros((1, STEPS_PER_SAMPLE, NUM_FEATURES), dtype=float)
    timeStep = STEPS_PER_SAMPLE - SIZE_OF_SUBSET
    uart.reset()
    while True:
        MLInput[0, timeStep, ::] = get_uart_data(uart)
        timeStep += 1
        # print("timestep", timeStep)
        if timeStep >= STEPS_PER_SAMPLE:
            MLInputQueue.put(MLInput)
            MLInput[0, :-SIZE_OF_SUBSET, ::] = MLInput[0, SIZE_OF_SUBSET:, ::]
            timeStep = STEPS_PER_SAMPLE - SIZE_OF_SUBSET
            uart.reset()

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
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model_w_nothing.keras')

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
        if pred[0, predictedClass] > 0.9:
            print(f"class is {predictedClass}, prob: {pred[0, predictedClass]}")
        else:
            print(f"MAYBE class {predictedClass}, prob: {pred[0, predictedClass]}")
        # gui.update()
        # except:
            # pass # the MLInput is currently not ready

