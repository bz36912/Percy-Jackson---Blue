import paho.mqtt.client as mqtt
import threading
from queue import Queue

mqttTxDataQueue = Queue(30)

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

def send_message(mqttc, message):
    unacked_publish = set()
    mqttc.user_data_set(unacked_publish)
    # message should come from the receive data queue
    msg_info = mqttc.publish("un47043712", message, qos=1)
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()

def mqtt_entry():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_publish = on_publish
    mqttc.user_data_set([])
    mqttc.connect("csse4011-iot.zones.eait.uq.edu.au")
    mqttc.loop_forever()
    print(f"Received the following message: {mqttc.user_data_get()}")


def mqtt_thread_start():
    mqttThread = threading.Thread(target=mqtt_entry)
    mqttThread.start()