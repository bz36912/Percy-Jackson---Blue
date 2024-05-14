import tkinter as tk
from gui import GUI
from uart import Uart
import time
import tensorflow as tf
from tensorflow import keras
import threading
from ML_predict import UART_polling_thread_entry, MLInputQueue
import numpy as np
import enum

root = tk.Tk()
gui = GUI(root)

if __name__ == "__main__":
    
    # Example of changing label text
    gui.set_label_text("New X Value", "New Y Value", "New Z Value")
    try:
        uart = Uart('COM7') # Change depending on thing
    except:
        uart = Uart('/dev/tty.usbmodem0010502493171')
    startTime = time.time()
    t = startTime
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model.keras')
    # activity_classifier.summary()

    uartThread = threading.Thread(target=UART_polling_thread_entry, args=(uart,))
    uartThread.start()
    while True:
        # ret = uart.get_acceleration()
        ret = None
        if ret is not None:
            x, y, z = ret
            timeStamp = round(time.time() - startTime, 3)
            print(f"the acceleration is ({x}, {y}, {z}) ms-2, time: {timeStamp}")
            if (time.time() - t) > 0.5:
                gui.set_label_text(str(x), str(y), str(z))
                t = time.time()
            gui.update()

        try:
            MLInput = MLInputQueue.get(block=False)
            pred = activity_classifier.predict(MLInput)
            predictedClass = np.argmax(pred)
            if pred[0, predictedClass] > 0.6:
                print(pred, "predicted class is", predictedClass)
            else:
                print("prediction is UNCERTAIN")
            gui.update()
        except:
            pass # the MLInput is currently not ready