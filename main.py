# main.py -- put your code here!
# main.py -- put your code here!
from umqtt.simple import MQTTClient
from machine import Pin

import ujson
import network
import utime as time
import dht

import auth
from hardware import DEVICE_ID, DHT_PIN, RED_LED, YELLOW_LED


# ----------------- Power on --------------------------------
RED_LED.on()


# ----------------- Wi-Fi setup ----------------------------
WIFI_SSID             = auth.WIFI_SSID
WIFI_PASSWORD         = auth.WIFI_PASSWORD


# ----------------- MQTT setup ----------------------------
MQTT_BROKER           = "mqtt-dashboard.com"
MQTT_CLIENT           = DEVICE_ID
MQTT_TELEMETRY_TOPIC  = "iot/telemetry"
MQTT_CONTROL_TOPIC    = "iot/control"


# --------------- Setup done -------------------------------
YELLOW_LED.on()


# ---------------- methods -----------------------------------
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


def create_json_data(temp, humidity):
    data = ujson.dumps({
        "temp": temp,
        "humidity": humidity,
    })
    
    return data


def mqtt_client_publish(topic, data):
    print('\n Updatimng MQTT Broker...\n')
    mqtt_client.publish(topic, data)
    print(data)


def send_led_status():
    data = ujson.dumps({
        "red_led": "ON" if RED_LED.value() == 1 else "OFF",
        "yellow_led": "ON" if YELLOW_LED.value() == 1 else "OFF",
    })
    mqtt_client_publish(MQTT_TELEMETRY_TOPIC, data)


# ------------------- main --------------------------------------

# Connect to Wi-Fi
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print('\n Connecting the device to WiFi...\n')
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)


# Wait for Wi-Fi connection
while not wifi_client.isconnected():
    print('Connecting to Wi-Fi... \n')
    time.sleep(1)
print('Wi-Fi connected successfully')
print(wifi_client.ifconfig())           # Get/set IP-level network interface parameters


# Connect to MQTT
mqtt_client = mqtt_connect()
RED_LED.off()
YELLOW_LED.off()
dht_sensor = dht.DHT22(DHT_PIN)

telemetry_data_old = ''
telemetry_data_new = ''

# ---------------- main loop ---------------------------------
while True:
    mqtt_client.check_msg()             # Check if the server has any pending messages
    print('. ', end="")
    
    try:
        dht_sensor.measure()
        time.sleep(5)
        telemetry_data_new = create_json_data(dht_sensor.temperature(), dht_sensor.humidity())
    except OSError:
        print("cant read")

    if telemetry_data_new != telemetry_data_old:
        mqtt_client_publish(MQTT_TELEMETRY_TOPIC, telemetry_data_new)
        telemetry_data_old = telemetry_data_new

    time.sleep(0.1)

