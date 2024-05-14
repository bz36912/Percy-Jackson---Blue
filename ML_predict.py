from data_log import get_uart_data, STEPS_PER_SAMPLE, NUM_FEATURES
from uart import Uart
from queue import Queue
import numpy as np
SIZE_OF_SUBSET = 31
import threading

MLInputQueue = Queue()
def UART_polling_thread_entry(uart):
    MLInput = np.zeros((1, STEPS_PER_SAMPLE, NUM_FEATURES), dtype=float)
    timeStep = 0
    while True:
        MLInput[0, timeStep, ::] = get_uart_data(uart)
        timeStep += 1
        if timeStep >= STEPS_PER_SAMPLE:
            MLInputQueue.put(MLInput)
            MARGIN = 2
            MLInput[0, :-SIZE_OF_SUBSET, ::] = MLInput[0, SIZE_OF_SUBSET:, ::]
            timeStep = STEPS_PER_SAMPLE - SIZE_OF_SUBSET

if __name__ == "__main__":
    try:
        uart = Uart('COM7') # Change depending on thing
    except:
        try:
            uart = Uart('/dev/tty.usbmodem0010502493171')
        except:
            uart = Uart('COM15')
    uartThread = threading.Thread(target=UART_polling_thread_entry, args=(uart,))
    uartThread.start()

    while True:
        data = MLInputQueue.get(block=True)
        print("first timestep", data[0, 0, ::])
        print("last timestep", data[0, -1, ::])

