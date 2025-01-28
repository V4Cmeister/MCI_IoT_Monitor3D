import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from credentials import MQTT_USERNAME, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT
import os
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s - %(asctime)s')
logger = logging.getLogger()

# Initialize TinyDB
db_path = 'db/filament_weight.json'
if not os.path.exists('db'):
    os.makedirs('db')
if not os.path.exists(db_path) or os.stat(db_path).st_size == 0:
    with open(db_path, 'w') as f:
        json.dump({}, f)  # Initialize with an empty dictionary

db = TinyDB(db_path)
Weight = Query()

last_processed_time = datetime.now() - timedelta(minutes=1)

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe("Filament_Supervision/filament_weight")
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global last_processed_time
    current_time = datetime.now()
    if current_time - last_processed_time >= timedelta(minutes=1):
        try:
            weight = float(msg.payload.decode())
            timestamp = current_time.isoformat()
            db.insert({'timestamp': timestamp, 'weight': weight})
            logger.debug(f"Data inserted: {weight}g")
            last_processed_time = current_time
        except ValueError as e:
            logger.error(f"Error decoding message: {e}")

def mqtt_loop():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    mqtt_loop()