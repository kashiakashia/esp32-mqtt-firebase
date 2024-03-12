from machine import Pin, ADC
import dht


# -----------------  Device setup --------------------------
DEVICE_ID             = "detector_001"

# ----------------- DHT sensor setup -----------------------
DHT_PIN = Pin(15)
dht_sensor = dht.DHT22(DHT_PIN)

# -------------- Photo Resistor (LDR) setup ----------------
LDR = Pin(34)
ldr_adc = ADC(LDR)

# ----------------- LED setup ------------------------------
RED_LED = Pin (13, Pin.OUT)
YELLOW_LED = Pin(12, Pin.OUT)
FLASH_LED   = Pin(2, Pin.OUT)