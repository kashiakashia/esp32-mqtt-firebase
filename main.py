from umqtt.simple import MQTTClient
import network
import utime as time

from hardware import DEVICE_ID, dht_sensor, RED_LED, YELLOW_LED, FLASH_LED
from mqtt import MQTT_BROKER, MQTT_CLIENT, MQTT_TELEMETRY_TOPIC, MQTT_CONTROL_TOPIC
from data_functions import create_json_data, send_led_status
from mqtt_functions import mqtt_client_publish
from wifi import wifi_connect
from auth import MQTT_USER, MQTT_PASSWORD, MQTT_BROKER 

global mqtt_client
telemetry_data_old = ''


# ------------------------ callback and connect mqtt functions ---------------------------------------------------
def mqtt_connect(user, password):
    print('Connection in progress...\n')
    mqtt_client = MQTTClient(MQTT_CLIENT, MQTT_BROKER, user=user, 
    password=password, ssl=True, ssl_params={'server_hostname': MQTT_BROKER})
    mqtt_client.set_callback(did_recieve_callback)
    mqtt_client.connect()
    print('Connected successfully \n')
    mqtt_client.subscribe(MQTT_CONTROL_TOPIC)
    
    return mqtt_client


def did_recieve_callback(topic, message):
    print('\n\nData Recieved! \ntopic = {0}, message = {1}'.format(topic, message))

    # device_id/lamp/color/state
    # device_id/lamp/state
    # lamp/state
    if topic == MQTT_CONTROL_TOPIC.encode():
        if message == ('{0}/lamp/yellow/on'.format(DEVICE_ID)).encode():
            YELLOW_LED.on()
        elif message == ('{0}/lamp/yellow/off'.format(DEVICE_ID)).encode():
            YELLOW_LED.off()
        elif message == ('{0}/lamp/red/on'.format(DEVICE_ID)).encode():
            RED_LED.on()
        elif message == ('{0}/lamp/red/off'.format(DEVICE_ID)).encode():
            RED_LED.off()
        elif message == ('{0}/lamp/on'.format(DEVICE_ID)).encode() or message == b'lamp/on':
            YELLOW_LED.on()
            RED_LED.on()
        elif message == ('{0}/lamp/off'.format(DEVICE_ID)).encode() or message == b'lamp/off':
            YELLOW_LED.off()
            RED_LED.off()
        elif message == ('{0}/status'.format(DEVICE_ID)).encode() or message == ('status').encode():
            global telemetry_data_old
            mqtt_client_publish(MQTT_TELEMETRY_TOPIC, telemetry_data_old, mqtt_client)
        else:
            return
        
        send_led_status(mqtt_client)

# ----------------------------- end of callback and connect mqtt functions -----------------------------------


# ----------------------------- Main ------------------------------------------
YELLOW_LED.on()
RED_LED.on()

wifi_connect()

# Connect to MQTT
mqtt_client = mqtt_connect(MQTT_USER, MQTT_PASSWORD)
mqtt_client_publish(MQTT_CONTROL_TOPIC, 'lamp/off', mqtt_client)        #clears the mqtt cache

YELLOW_LED.off()
RED_LED.off()


# ------------------- main loop --------------------------------------
while True:
    mqtt_client.check_msg()
    print(". ", end="")
    FLASH_LED.on()
    
    try:
        dht_sensor.measure()
        time.sleep(5)
        telemetry_data_new = create_json_data(dht_sensor.temperature(), dht_sensor.humidity())
    except OSError:
        print("cant read")
    
    time.sleep(0.5)
    FLASH_LED.off()

    telemetry_data_new = create_json_data(dht_sensor.temperature(), dht_sensor.humidity())

    if telemetry_data_new != telemetry_data_old:
        mqtt_client_publish(MQTT_TELEMETRY_TOPIC, telemetry_data_new, mqtt_client)
        telemetry_data_old = telemetry_data_new

    time.sleep(0.1)
