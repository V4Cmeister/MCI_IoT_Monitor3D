import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from src.credentials import MQTT_USERNAME, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT
import os
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Initialize TinyDB
db_path = '../db/filament_weight.json'
if not os.path.exists('db'):
    os.makedirs('db')
if not os.path.exists(db_path) or os.stat(db_path).st_size == 0:
    with open(db_path, 'w') as f:
        json.dump({}, f)  # Initialize with an empty dictionary

db = TinyDB(db_path)
Weight = Query()

last_processed_time = datetime.now() - timedelta(minutes=1)
Filament_sensor_up = False

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe("Filament_Supervision/filament_weight")
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global last_processed_time, Filament_sensor_up
    current_time = datetime.now()
    if current_time - last_processed_time >= timedelta(minutes=1):
        try:
            weight = float(msg.payload.decode())
            timestamp = current_time.isoformat()
            db.insert({'timestamp': timestamp, 'weight': weight})
            logger.debug(f"Data inserted: {timestamp}, {weight}g")
            last_processed_time = current_time
            Filament_sensor_up = True
        except ValueError as e:
            logger.error(f"Error decoding message: {e}")

def check_sensor_status():
    global Filament_sensor_up
    while True:
        current_time = datetime.now()
        if current_time - last_processed_time >= timedelta(minutes=1):
            if Filament_sensor_up:
                Filament_sensor_up = False
            else:
                timestamp = current_time.isoformat()
                db.insert({'timestamp': timestamp, 'weight': 0})
                logger.warning("No new data received from the filament sensor. Inserted 0g.")
        time.sleep(60)

def mqtt_loop():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    check_sensor_status()

if __name__ == "__main__":
    mqtt_loop()