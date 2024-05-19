import tkinter as tk
from gui import GUI
from uart import Uart
import time
import tensorflow as tf
from tensorflow import keras
import threading
from ML_predict import UART_polling_thread_entry, MLInputQueue
import numpy as np

root = tk.Tk()
gui = GUI(root)



if __name__ == "__main__":
    
    # Example of changing label text
    try:
        uart = Uart('COM7') # Change depending on thing
    except:
        try:
            uart = Uart('/dev/tty.usbmodem0010502493171')
        except:
            uart = Uart('COM15')
    startTime = time.time()
    t = startTime
    # activity_classifier = tf.keras.models.load_model('model1/activity_classification_model.keras')
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model_CNN_expanded.keras')
    # activity_classifier.summary()

    uartThread = threading.Thread(target=UART_polling_thread_entry, args=(uart,))
    uartThread.start()
    gui.update()
    while True:        
        MLInput = MLInputQueue.get(block=True)
        pred = activity_classifier.predict(MLInput)
        predictedClass = np.argmax(pred)
        if pred[0, predictedClass] > 0.5:
            print(pred, "predicted class is", predictedClass)
            if predictedClass != 4:
                gui.change_images(predictedClass)
                gui.output_text_message(str(np.max(pred)))
                gui.update()
            # else:
            #     gui.output_text_message("")
            #     gui.update()
        else:
            print("prediction is UNCERTAIN class", predictedClass, pred[0, predictedClass])
        
        