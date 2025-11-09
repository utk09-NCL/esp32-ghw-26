import socket
import network
import time
from machine import Pin

led = Pin(2, Pin.OUT)  # On-board LED for status indication


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f" Connected to WiFi. IP: {ip}")
        return ip

    SSID = "YOUR_WIFI_NAME"  # TODO: Replace with your WiFi SSID
    PASSWORD = "YOUR_WIFI_PASSWORD"  # TODO: Replace with your WiFi password

    print(f" Connecting to WiFi {SSID}...")
    wlan.connect(SSID, PASSWORD)

    for _ in range(10):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f" Connected to WiFi. IP: {ip}")
            return ip
        time.sleep(1)
        print(" Attempting to connect...")

    print(" Failed to connect to WiFi.")
    return None
