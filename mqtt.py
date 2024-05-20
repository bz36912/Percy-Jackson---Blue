"""
MQTT.py written by Daniel Barone
This program is called by a seperate thread in the main.py file.
This program connects to the host specified in the "broker" variable and publishes to the topic defined by the "topic" variables
Running mqtt_thread_start() in the main file, as well as adding to the mqttTxDataQueue queue will allow the program to publish any
of the values passed into the queue
"""


import paho.mqtt.client as mqtt
import threading
from queue import Queue

# MQTT broker information
broker = "csse4011-iot.zones.eait.uq.edu.au"
port = 1883
topic = "un47043712"

mqttTxDataQueue = Queue(30)

def publish_input(client):
    while True:
        msg = mqttTxDataQueue.get() # Get the message from the queue
        client.publish(topic, str(msg)) # Publish the message to the specified topic via MQTT


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def mqtt_entry():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # initialise the client variable
    client.on_connect = on_connect # Defines the function called when the program connects
    client.user_data_set([])
    client.connect(broker) # Connects the user to the broker
    try:
        publish_input(client)
    finally:
        # Stop the MQTT loop and disconnect
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker")
    print(f"Received the following message: {client.user_data_get()}")

# Function called in the main.py file to start the thread of the MQTT program
# MQTT is done in a seperate thread because the functionality would block the excecution of the main thread if it wasn't a seperate thread
def mqtt_thread_start():
    mqttThread = threading.Thread(target=mqtt_entry)
    mqttThread.start()
