from hardware import DEVICE_ID
from auth import MQTT_BROKER

# MQTT Setup
MQTT_BROKER             = MQTT_BROKER       # secure Mqtt broker
MQTT_CLIENT             = DEVICE_ID
MQTT_TELEMETRY_TOPIC    = 'iot/device/{0}/telemetry'.format(DEVICE_ID)
MQTT_CONTROL_TOPIC      = 'iot/device/{0}/control'.format(DEVICE_ID)