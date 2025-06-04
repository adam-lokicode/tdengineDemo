import time
import random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

plants = ["plant1", "plant2", "plant3", "plant4"]

sensors = {
    "sensor1": lambda: f"temperature={random.uniform(20, 30):.2f},humidity={random.uniform(40, 60):.2f},vibration={random.uniform(0.1, 1.5):.2f}",
    "sensor2": lambda: f"temperature={random.uniform(25, 35):.2f},co2={random.uniform(400, 1000):.2f},noise={random.uniform(30, 80):.2f}"
}

while True:
    for plant in plants:
        for sensor_id, payload_func in sensors.items():
            topic = f"factory/{plant}/{sensor_id}"
            payload = payload_func()
            client.publish(topic, payload)
            print(f"Published to {topic}: {payload}")
    time.sleep(3)