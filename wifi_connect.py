import network  # Import the network module for WiFi functions
import time  # Import time module for delays and timeouts


def scan_networks():
    # STA_IF = station interface, connects to a WiFi network
    # AP_IF = access point interface, creates a WiFi network
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object in station (client) mode
    wlan.active(True)  # Activate the WiFi interface
    networks = wlan.scan()  # Scan for available WiFi networks

    for i, net in enumerate(networks):
        ssid = net[0].decode("utf-8")  # SSID (network name) as string
        bssid = ":".join(
            f"{b:02x}" for b in net[1]
        )  # BSSID (MAC address) in readable format
        channel = net[2]  # WiFi channel number
        rssi = net[3]  # Signal strength (dBm)
        security = net[4]  # Security type (0=open, 1=WEP, 2=WPA-PSK, etc.)
        hidden = bool(net[5])  # True if network is hidden

        # Choose lock icon if secured, dizzy face if open
        secure_icon = "🔒" if security > 0 else "😵"

        # Print info for each network
        print(
            f"{i + 1}. {secure_icon} SSID: {ssid:25} | BSSID: {bssid} | Channel: {channel} | RSSI: {rssi} dBm | Security: {security} | Hidden: {hidden}"
        )

    return networks  # Return the raw list of network info tuples


def connect_wifi(ssid, password, timeout=10):
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object in station mode
    wlan.active(True)  # Activate the interface
    if wlan.isconnected():  # If already connected
        print(f"Already connected to {wlan.config('essid')}")
        return wlan.ifconfig()[0]  # Return current IP address
    print(f"Connecting to '{ssid}'", end="")
    wlan.connect(ssid, password)  # Start connection
    start = time.time()  # Record start time
    while not wlan.isconnected():  # Wait until connected or timeout
        if time.time() - start > timeout:
            print("\nConnection timeout!")
            return None  # Return None if timeout
        print(".", end="")  # Print progress dot
        time.sleep(0.5)  # Wait before retrying
    ip_info = wlan.ifconfig()  # Get IP info after connection
    print("\nConnected!")
    print(f"  IP Address: {ip_info[0]}")  # ESP32's assigned IP
    print(f"  Gateway:    {ip_info[2]}")  # Router IP (internet access point)
    print(f"  DNS:        {ip_info[3]}")  # DNS server for domain name resolution
    return ip_info[0]  # Return IP address


def disconnect():
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object in station mode
    if wlan.isconnected():  # If connected
        wlan.disconnect()  # Disconnect from WiFi
        print("Disconnected")
    else:
        print("Not connected")  # Print if not connected


def status():
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object in station mode
    if wlan.isconnected():  # If connected
        print(f"Connected to: {wlan.config('essid')}")  # Print SSID
        print(f"IP Address: {wlan.ifconfig()[0]}")  # Print IP address
    else:
        print("Not connected")  # Print if not connected


if __name__ == "__main__":
    print("WiFi Connector")
    print("*" * 20)
    print("""
          Example usage:
          mpremote connect /dev/cu.usbserial-0001 repl
            >>> import wifi_connect
            >>> wifi_connect.scan_networks()
            >>> wifi_connect.connect_to_wifi('Your_SSID', 'Your_Password')
            """)
    print("*" * 20)
    print(":: scan_networks() - Find available WiFi networks")
    print(":: connect_to_wifi(ssid, password) - Connect to a WiFi network")
    print(":: status() - Show current connection status")
    print(":: disconnect() - Disconnect from current WiFi network")
    print("*" * 20)
