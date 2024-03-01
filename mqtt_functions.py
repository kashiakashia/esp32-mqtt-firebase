from umqtt.simple import MQTTClient
import network

from hardware import DEVICE_ID, RED_LED, YELLOW_LED
from mqtt import MQTT_BROKER, MQTT_CLIENT, MQTT_TELEMETRY_TOPIC, MQTT_CONTROL_TOPIC

global mqtt_client

# ---------------- mqtt methods -----------------------------------

def mqtt_client_publish(topic, data, mqtt_client):
    print('\n Updatimng MQTT Broker...\n')
    mqtt_client.publish(topic, data)
    print(data)


