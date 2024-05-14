import tkinter as tk
from gui import GUI
from uart import Uart
import time
import tensorflow as tf
from tensorflow import keras


root = tk.Tk()
gui = GUI(root)


if __name__ == "__main__":
    
    # Example of changing label text
    # gui.set_label_text("New X Value", "New Y Value", "New Z Value")
    # try:
    #     uart = Uart('COM7') # Change depending on thing
    # except:
    #     uart = Uart('/dev/tty.usbmodem0010502493171') 
    startTime = time.time()
    t = startTime
    activity_classifier = tf.keras.models.load_model('model1/activity_classification_model.keras')
    # activity_classifier.summary()
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