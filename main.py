# main.py -- put your code here!
from umqtt.simple import MQTTClient
from machine import Pin

import ujson
import network
import utime as time
import dht

import auth
from hardware import DEVICE_ID, DHT_PIN, RED_LED, YELLOW_LED
from auth import WIFI_SSID, WIFI_PASSWORD
from mqtt_functions import recieved_callback, mqtt_connect, mqtt_client_publish, send_led_status
from data_functions import create_json_data


# ----------------- Power on --------------------------------
RED_LED.on()


# ----------------- MQTT setup ----------------------------
MQTT_BROKER           = "mqtt-dashboard.com"

MQTT_TELEMETRY_TOPIC  = "iot/telemetry"
MQTT_CONTROL_TOPIC    = "iot/control"


# --------------- Setup done -------------------------------
YELLOW_LED.on()



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
        YELLOW_LED.on()
        mqtt_client_publish(MQTT_TELEMETRY_TOPIC, telemetry_data_new, mqtt_client)
        telemetry_data_old = telemetry_data_new
        YELLOW_LED.off()

    time.sleep(0.1)

