import os
import time
import taosrest
import paho.mqtt.client as mqtt

# TDengine Cloud credentials from environment
TDENGINE_URL = os.environ["TDENGINE_CLOUD_URL"]
TDENGINE_TOKEN = os.environ["TDENGINE_CLOUD_TOKEN"]

# Connect to TDengine Cloud
conn = taosrest.connect(url=TDENGINE_URL, token=TDENGINE_TOKEN)
cursor = conn.cursor()

# MQTT setup
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/+/+"  # Subscribe to all simulated sensors

# Allowed plants for filtering
VALID_PLANTS = {"plant1", "plant2", "plant3", "plant4"}

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 3:
            return

        _, plant, sensor = topic_parts

        if plant not in VALID_PLANTS:
            return

        payload = msg.payload.decode()
        values = {
            kv.split("=")[0]: float(kv.split("=")[1])
            for kv in payload.split(",")
            if "=" in kv
        }

        # If no valid values, skip
        if not values:
            print(f"⚠️ No values to insert from topic: {msg.topic}")
            return

        ts = int(time.time() * 1000)
        table_name = f"{plant}_{sensor}"

        cursor.execute("USE factory")  # Ensure DB context

        expected_columns = ["temperature", "humidity", "vibration", "co2", "noise"]
        column_values = ", ".join(str(values.get(col, "null")) for col in expected_columns)

        sql = (
            f"INSERT INTO factory.{table_name} USING factory.sensors TAGS ('{plant}', '{sensor}') "
            f"VALUES ({ts}, {column_values})"
        )

        print("📤 Executing SQL:", sql)
        cursor.execute(sql)

    except Exception as e:
        print("❌ Error processing message:", e)

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔁 Connecting to MQTT broker...")
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_forever()