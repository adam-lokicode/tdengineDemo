import time
import random
import paho.mqtt.client as mqtt
import taos

# TDengine Cloud connection parameters
TDENGINE_HOST = 'your-cloud.tdengine.cloud'
TDENGINE_USER = 'your-username'
TDENGINE_PASSWORD = 'your-password'
TDENGINE_DATABASE = 'factory'

# Connect to TDengine
conn = taos.connect(
    host=TDENGINE_HOST,
    user=TDENGINE_USER,
    password=TDENGINE_PASSWORD,
    database=TDENGINE_DATABASE
)
cursor = conn.cursor()

# MQTT configuration
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'factory/sensor1'

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        values = {kv.split('=')[0]: float(kv.split('=')[1]) for kv in payload.split(',')}
        ts = int(time.time() * 1000)
        sql = f"INSERT INTO sensor1 USING sensors TAGS ('plant1') VALUES ({ts}, {values['temperature']}, {values['humidity']}, {values['vibration']})"
        print("Executing SQL:", sql)
        cursor.execute(sql)
    except Exception as e:
        print("Error processing message:", e)

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()