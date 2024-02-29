from umqtt.simple import MQTTClient
from machine import Pin
from hardware import DEVICE_ID, DHT_PIN, RED_LED, YELLOW_LED

import ujson
import network
import utime as time

from hardware import DEVICE_ID

# ----------------- MQTT setup ----------------------------
MQTT_CLIENT           = DEVICE_ID
MQTT_BROKER           = "mqtt-dashboard.com"
MQTT_TELEMETRY_TOPIC  = "iot/telemetry"
MQTT_CONTROL_TOPIC    = "iot/control"


# ---------------- mqtt methods -----------------------------------

def recieved_callback(topic, message):
    print('\n\n Message recieved. \nTopic: {0}, message: {1}'.format(topic, message))

    # message format:
    # device_id/lamp/color/state
    # device_id/lamp/state
    # lamp/state

    if topic == MQTT_CONTROL_TOPIC.encode():   # encode() is to change the string to bytes, as we get bytes from the cloud
        if message == ('{0}/lamp/red/on'.format(DEVICE_ID)).encode():
            RED_LED.on()
        elif message == ('{0}/lamp/red/off'.format(DEVICE_ID)).encode():
            RED_LED.off()
        elif message == ('{0}/lamp/yellow/on'.format(DEVICE_ID)).encode():
            YELLOW_LED.on()
        elif message == ('{0}/lamp/yellow/off'.format(DEVICE_ID)).encode():
            YELLOW_LED.off()
        elif message == ('{0}/lamp/on'.format(DEVICE_ID)).encode() or message == 'lamp/on'.encode():
            YELLOW_LED.on()
            RED_LED.on()
        elif message == ('{0}/lamp/off'.format(DEVICE_ID)).encode() or message == 'lamp/off'.encode():
            YELLOW_LED.off()
            RED_LED.off()
        else:
            return
        
        send_led_status()


def mqtt_connect():
    print('Connection in progress...\n')
    mqtt_client = MQTTClient(MQTT_CLIENT, MQTT_BROKER, user="", 
    password="")
    mqtt_client.set_callback(recieved_callback)
    mqtt_client.connect()
    print('Connected successfully \n')
    mqtt_client.subscribe(MQTT_CONTROL_TOPIC)
    
    return mqtt_client


def mqtt_client_publish(topic, data, mqtt_client):
    print('\n Updatimng MQTT Broker...\n')
    mqtt_client.publish(topic, data)
    print(data)


def send_led_status():
    data = ujson.dumps({
        "red_led": "ON" if RED_LED.value() == 1 else "OFF",
        "yellow_led": "ON" if YELLOW_LED.value() == 1 else "OFF",
    })
    mqtt_client_publish(MQTT_TELEMETRY_TOPIC, data)