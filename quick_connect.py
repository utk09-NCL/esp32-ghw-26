from wifi_connect import connect_wifi


def quick_connect():
    SSID = "YOUR_WIFI_NAME"  # TODO: Replace with your WiFi SSID
    PASSWORD = "YOUR_WIFI_PASSWORD"  # TODO: Replace with your WiFi password
    return connect_wifi(SSID, PASSWORD)  # Connect using predefined credentials


if __name__ == "__main__":
    print("Quick WiFi Connector")
    print("*" * 25)
    print("Attempting to connect using predefined SSID and PASSWORD...")
    ip_address = quick_connect()
    if ip_address:
        print(f"Successfully connected! IP Address: {ip_address}")
    else:
        print("Failed to connect to WiFi.")
    print("*" * 25)
