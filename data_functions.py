import ujson
from hardware import DEVICE_ID, YELLOW_LED, RED_LED
from mqtt import MQTT_TELEMETRY_TOPIC

from mqtt_functions import mqtt_client_publish



# ---------------- data methods -----------------------------------

def create_json_data(temp, humidity):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "temp": temp,
        "humidity": humidity,
        "type" : "sensor",
    })
    
    return data


def send_led_status(mqtt_client):

    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "YELLOW_LED": "ON" if YELLOW_LED.value() == 1 else "OFF",
        "RED_LED": "ON" if RED_LED.value() == 1 else "OFF",
        "type": "lamp"
    })
    mqtt_client_publish(MQTT_TELEMETRY_TOPIC, data, mqtt_client)