from machine import Pin


# -----------------  Device setup --------------------------
DEVICE_ID             = "detector_001"

# ----------------- DHT sensor setup -----------------------
DHT_PIN = Pin(15)


# ----------------- LED setup ------------------------------
RED_LED = Pin (13, Pin.OUT)
YELLOW_LED = Pin(12, Pin.OUT)