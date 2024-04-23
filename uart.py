import serial
import matplotlib.pyplot as plt
import threading
from queue import Queue

uartTxQueue = Queue(30)
uartRxDataQueue = Queue(30)
uartRxConfigQueue = Queue(30)

class Uart:
    def __init__(self, port:str) -> None:
        self.ser = serial.Serial(port, 115200, timeout=1)

        print("Uart:__init__(): starting the UART thead")
        shellThread = threading.Thread(target=self.thread_entry)
        shellThread.start()

    def thread_entry(self):
        while True:
            # listen to the port
            line = self.ser.readline().decode().strip()
            self.process_line(line)

            # check the TX queue
            try:
                string:str = uartTxQueue.get_nowait() + "\n"
                print("UART sending:", string)
                self.ser.write(string.encode())
            except: # empty exception is raised, and nothing to be sent
                pass

    def process_line(self, line):
        if len(line) == 0:
            return
        
        try:
            data = eval(line)

            x, y, z = data['x'], data['y'], data['z']
            print(f"the acceleration is ({x}, {y}, {z}) ms-2")
        except:
            return

if __name__ == "__main__":
    uart = Uart('/dev/tty.usbmodem0010502493171') # '/dev/tty.usbmodem0010502493171'
