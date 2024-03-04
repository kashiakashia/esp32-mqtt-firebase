from hardware import DEVICE_ID

# MQTT Setup
MQTT_BROKER           = "mqtt-dashboard.com"
MQTT_CLIENT             = DEVICE_ID
MQTT_TELEMETRY_TOPIC    = 'iot/device/{0}/telemetry'.format(DEVICE_ID)
MQTT_CONTROL_TOPIC      = 'iot/device/{0}/control'.format(DEVICE_ID)