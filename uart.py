"""
uart.py written by Bolong Zhang
Controls the UART. Fetches data from the NRF52840 board.
"""
import serial
import matplotlib.pyplot as plt
import threading
from queue import Queue
import time

class Uart:
    def __init__(self, port:str) -> None:
        """initialise UART and pyserial

        Args:
            port (str): the name of the port
        """
        self.ser = serial.Serial(port, 115200, timeout=1)
        print("Uart:__init__()")
        
    def process_line(self, line, getIdex=False):
        """extracts x, y, z and index values from UART message.

        Args:
            line (str): the line of UART message
            getIdex (bool, optional): If the index number of the transmission is returned. 
            The index marks the chronogical order of the UART transmission. Defaults to False.

        Returns:
            x, y, z, index. None on error.
        """
        if len(line) == 0:
            return None
        
        try:
            data = eval(line) 
            # data is of the time of dictionary, since line is the string representatio of a dictionary
            if getIdex:
                return data['x'], data['y'], data['z'], data['index']
            else:
                return data['x'], data['y'], data['z']
        except:
            return None
        
    def get_acceleration(self, getIdex=False):
        """Reads from UART and extracts the x, y, z accelerations and the index of the transmission

        Args:
            getIdex (bool, optional): If the index number of the transmission is returned. 
            The index marks the chronogical order of the UART transmission. Defaults to False.

        Returns:
            x, y, z, index. None on error. 
        """
        line = self.ser.readline().decode().strip()
        # each line contains the accelerations in x, y and z axis
        return self.process_line(line, getIdex)
    
    def reset(self):
        """resets the UART RX buffer to prevent the buffer from overflowing
        """
        self.ser.reset_input_buffer()

# the code below is testing this subsystem by itself. The below code will be used
# when the subsystem is called from main.py
if __name__ == "__main__":
    uart = Uart('/dev/tty.usbmodem0010502493171') # '/dev/tty.usbmodem0010502493171'
    startTime = time.time()
    while True:
        ret = uart.get_acceleration()
        if ret is not None:
            x, y, z = ret
            timeStamp = round(time.time() - startTime, 3)
            print(f"the acceleration is ({x}, {y}, {z}) ms-2, time: {timeStamp}")
