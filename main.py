import tkinter as tk
from gui import GUI
from uart import Uart
import time

root = tk.Tk()
gui = GUI(root)


if __name__ == "__main__":
    
    # Example of changing label text
    # gui.set_label_text("New X Value", "New Y Value", "New Z Value")
    uart = Uart('COM7')# Change depending on thing
    startTime = time.time()
    t = startTime
    while True:
        ret = uart.get_acceleration()
        if ret is not None:
            x, y, z = ret
            timeStamp = round(time.time() - startTime, 3)
            print(f"the acceleration is ({x}, {y}, {z}) ms-2, time: {timeStamp}")
            if (time.time() - t) > 0.5:
                gui.set_label_text(str(x), str(y), str(z))
                t = time.time()
            gui.update()
            # time.sleep(1)