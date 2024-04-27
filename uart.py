import serial
import matplotlib.pyplot as plt
import threading
from queue import Queue
import time

class Uart:
    def __init__(self, port:str) -> None:
        self.ser = serial.Serial(port, 115200, timeout=1)
        print("Uart:__init__()")
        
    def process_line(self, line):
        if len(line) == 0:
            return None
        
        try:
            data = eval(line)
            return data['x'], data['y'], data['z']
        except:
            return None
        
    def get_acceleration(self):
        line = self.ser.readline().decode().strip()
        return self.process_line(line)

if __name__ == "__main__":
    uart = Uart('/dev/tty.usbmodem0010502493171') # '/dev/tty.usbmodem0010502493171'
    startTime = time.time()
    while True:
        ret = uart.get_acceleration()
        if ret is not None:
            x, y, z = ret
            timeStamp = round(time.time() - startTime, 3)
            print(f"the acceleration is ({x}, {y}, {z}) ms-2, time: {timeStamp}")
