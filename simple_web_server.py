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


def web_page():
    led_state = "ON" if led.value() == 1 else "OFF"
    status_color = "green" if led.value() == 1 else "red"
    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ESP32 LED Controller</title>
    <style>
      body {{ font - family: Arial, Helvetica, sans-serif; padding: 50px; overflow: hidden; text-align: center;}}
      h1 {{ color: #333;}}
      .status {{ font - size: 24px; color: {status_color}; margin: 30px; }}
      a {{ display: inline-block; padding: 15px 30px; margin: 10px; font-size: 20px; color: white; text-decoration: none; border-radius: 5px; }}
      .on {{ background - color: darkgreen; }}
      .off {{ background - color: darkred; }}
    </style>
  </head>
  <body>
    <h1>ESP32 LED Controller</h1>
    <div class="status">LED is currently: <strong>{led_state}</strong></div>
    <a href="/on" class="on">Turn ON</a>
    <a href="/off" class="off">Turn OFF</a>
  </body>
</html>
"""
    return html


def start_server():
    ip = connect_wifi()
    if not ip:
        print("Could not connect to WiFi. Exiting...")
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 80))
    s.listen(5)
    print(f"\n Listening on http://{ip}:80")
    print(" Press Ctrl+C to stop the server.\n")

    try:
        while True:
            conn, addr = s.accept()
            print(f" Connection from {addr}")

            request = conn.recv(1024).decode()
            print(f" Request: {request}")

            if "/on" in request:
                led.on()
                print(" LED turned ON")
            elif "/off" in request:
                led.off()
                print(" LED turned OFF")

            response = "HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n"
            response += web_page()

            conn.sendall(response.encode())
            conn.close()
    except KeyboardInterrupt:
        print(" Server stopped.")
        s.close()
        led.off()


if __name__ == "__main__":
    start_server()
