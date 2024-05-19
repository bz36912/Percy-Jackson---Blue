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
        msg = mqttTxDataQueue.get()
        # Publish the user input to the specified topic
        client.publish(topic, str(msg))
        # print(f"Message '{msg}' sent to topic '{topic}'")


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def mqtt_entry():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.user_data_set([])
    client.connect(broker)
    try:
        # Run the publish_input function in the main thread
        publish_input(client)
    finally:
        # Stop the MQTT loop and disconnect
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker")
    print(f"Received the following message: {client.user_data_get()}")


def mqtt_thread_start():
    mqttThread = threading.Thread(target=mqtt_entry)
    mqttThread.start()
