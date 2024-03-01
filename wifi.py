import network
import utime as time

from auth import WIFI_PASSWORD, WIFI_SSID

def wifi_connect():
    # Connect to WiFi
    wifi_client = network.WLAN(network.STA_IF)
    wifi_client.active(True)
    print("Connecting device to WiFi")
    wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for Wi-Fi connection
    while not wifi_client.isconnected():
        print('Connecting to Wi-Fi... \n')
        time.sleep(1)
    print('Wi-Fi connected successfully')
    print(wifi_client.ifconfig())               # Get/set IP-level network interface parameters