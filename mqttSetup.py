import time
import random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

while True:
    payload = f"temperature={random.uniform(20, 30):.2f},humidity={random.uniform(40, 60):.2f},vibration={random.uniform(0.1, 1.5):.2f}"
    client.publish("factory/sensor1", payload)
    print("Published:", payload)
    time.sleep(2)