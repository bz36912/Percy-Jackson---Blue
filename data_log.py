'''
data_log.py written by Bolong (Jack) Zhang
data_log.py is the program used to record data points.
There are two modes for recording data: continous sampling and toggled sampling
For the models created, toggled sampling was used for the sitting and standing data whereas continous was used for running and walking
This file is ran independintly of the main.py file
If users want to collect more data, they can modify the macros defined at the beginning of the file
and define whether they are using toggled or continous sampling
'''

from uart import Uart
import time
import numpy as np
import matplotlib.pyplot as plt
import keyboard

NUM_SAMPLES_PER_CLASS = 75
SAMPLING_WINDOW_DURATION = 3 # sec
SAMPLING_FREQUENCY = 40 # Hz
NUM_FEATURES = 3
STEPS_PER_SAMPLE = SAMPLING_WINDOW_DURATION * SAMPLING_FREQUENCY
NUM_TIMESTEPS = NUM_SAMPLES_PER_CLASS * STEPS_PER_SAMPLE

prevIndex = 0

def get_uart_data(uart:Uart):
    global prevIndex
    ret = None
    for j in range(3):
        ret = uart.get_acceleration(getIdex=True)
        if ret is not None:
            x, y, z, index = ret
            if index - prevIndex >= 2:
                print("mismatch between prevIndex and index", prevIndex, index)
            prevIndex = index
            return [x, y, z]
    
    if ret is None:
        print("UART ret is None")
        return [0.0, 0.0, 0.0]

def visualise_data(data:np.ndarray):
    # visualise the data for debugging
    reshaped = data.reshape(-1, NUM_FEATURES)
    fig, axs = plt.subplots(NUM_FEATURES, 1)
    timeSteps = np.arange(reshaped.shape[0])
    majorTicks = np.arange(0, reshaped.shape[0] + 1, STEPS_PER_SAMPLE)
    for i in range(NUM_FEATURES):
        axs[i].plot(timeSteps, reshaped[::, i])
        axs[i].set_xticks(majorTicks)
        axs[i].grid(which='major', alpha=0.8)
    plt.show()

def continuous_sampling(uart:Uart, fileName):
    data = np.zeros((NUM_TIMESTEPS, NUM_FEATURES), dtype=float)
    startTime = time.time()
    sampleTime = time.time()

    uart.reset()
    for i in range(NUM_TIMESTEPS):
        data[i] = get_uart_data(uart)
        if i % (STEPS_PER_SAMPLE) == 0:
            print("collecting sample number:", i / (STEPS_PER_SAMPLE), time.time() - sampleTime)
            sampleTime = time.time()
    print("finished collecting data after", time.time() - startTime) # at home it take 156 sec for 50 samples

    visualise_data(data)

    # save the data to a .npy file
    data = data.reshape((NUM_SAMPLES_PER_CLASS, STEPS_PER_SAMPLE, NUM_FEATURES))
    np.save("data/" + fileName, data)

    return data

def toggle_sampling(uart:Uart, sittingFileName, standingFileName):
    sitData = np.zeros((NUM_TIMESTEPS, NUM_FEATURES), dtype=float)
    standData = np.zeros((NUM_TIMESTEPS, NUM_FEATURES), dtype=float)
    
    for i in range(NUM_SAMPLES_PER_CLASS):
        # collect sitting data
        print("SIT data sample", i)
        # pressing the "r" key starts the data collection

        while True:
            if keyboard.read_key() == "r":
                break
        
        uart.reset()
        sampleTime = time.time()
        for j in range(STEPS_PER_SAMPLE):
            sitData[i * STEPS_PER_SAMPLE + j] = get_uart_data(uart)
        print("completed SIT data sample", i, "time:", time.time() - sampleTime)
        
        # collect standing data
        print("STAND data sample", i)
        # pressing the "r" key starts the data collection

        while True:
            if keyboard.read_key() == "r":
                break
        
        uart.reset()
        sampleTime = time.time()
        for j in range(STEPS_PER_SAMPLE):
            standData[i * STEPS_PER_SAMPLE + j] = get_uart_data(uart)
        print("completed STAND data sample", i, "time:", time.time() - sampleTime)
    
    visualise_data(sitData)
    visualise_data(standData)

    # save the data to a .npy file
    sitData = sitData.reshape((NUM_SAMPLES_PER_CLASS, STEPS_PER_SAMPLE, NUM_FEATURES))
    np.save("data/" + sittingFileName, sitData)
    standData = standData.reshape((NUM_SAMPLES_PER_CLASS, STEPS_PER_SAMPLE, NUM_FEATURES))
    np.save("data/" + standingFileName, standData)

    return sitData, standData

if __name__ == "__main__":
    try:
        uart = Uart('COM7') # Change depending on thing
    except:
        try:
            uart = Uart('/dev/tty.usbmodem0010502493171')
        except:
            uart = Uart('COM15')

    # toggle_sampling(uart, "test", "ing")
    continuous_sampling(uart, "do_nothing_while_standing")


    
        

