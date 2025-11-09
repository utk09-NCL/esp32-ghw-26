# `wifi_connect.py` code output with instructions

This module provides WiFi connectivity functions for your ESP32. It allows you to scan available networks, connect to WiFi, check connection status, and disconnect.

## Prerequisites

- Your ESP32 must have MicroPython firmware installed (see [README.md](README.md))
- You must know your WiFi SSID (network name) and password
- You must have `mpremote` installed (see [README.md](README.md))

## Upload the `wifi_connect.py` file to your device

```bash
# Replace /dev/cu.usbserial-0001 with your device path
mpremote connect /dev/cu.usbserial-0001 fs cp wifi_connect.py :wifi_connect.py
```

## Method 1: Interactive usage via REPL

### Connect to the device REPL

```bash
mpremote connect /dev/cu.usbserial-0001 repl
```

### Sample output when connecting

```bash
# Connected to MicroPython at /dev/cu.usbserial-0001
# Use Ctrl-] or Ctrl-x to exit this shell

# raw REPL; CTRL-B to exit
# >
# MicroPython v1.26.1 on 2025-09-11; Generic ESP32 module with ESP32
# Type "help()" for more information.
```

### Scan available WiFi networks

```python
>>> import wifi_connect
>>> wifi_connect.scan_networks()
1. 🔒 Your_Home_Network           | BSSID: aa:bb:cc:dd:ee:ff | Channel: 6 | RSSI: -45 dBm | Security: 2 | Hidden: False
2. 🔒 Coffee_Shop_WiFi            | BSSID: 11:22:33:44:55:66 | Channel: 11 | RSSI: -67 dBm | Security: 2 | Hidden: False
3. 😵 Open_Network                | BSSID: 77:88:99:aa:bb:cc | Channel: 1 | RSSI: -72 dBm | Security: 0 | Hidden: False
```

**Legend:**

- 🔒 = Secured network (requires password)
- 😵 = Open network (no password required)
- RSSI = Signal strength in dBm (closer to 0 is stronger)
- Security: 0=Open, 1=WEP, 2=WPA-PSK, 3=WPA2-PSK, etc.

### Connect to a WiFi network

```python
>>> ip = wifi_connect.connect_wifi('Your_Home_Network', 'your_password')
Connecting to 'Your_Home_Network'....
Connected!
  IP Address: 192.168.1.100
  Gateway:    192.168.1.1
  DNS:        8.8.8.8
```

The function returns the IP address on success, or `None` on failure/timeout.

### Check connection status

```python
>>> wifi_connect.status()
Connected to: Your_Home_Network
IP Address: 192.168.1.100
```

### Disconnect from WiFi

```python
>>> wifi_connect.disconnect()
Disconnected
```

### Exit the REPL

```python
>>> # Press Ctrl+X or Ctrl+] to exit
```

---

## Method 2: Run as a standalone script

### Using the `run` command

```bash
mpremote connect /dev/cu.usbserial-0001 run wifi_connect.py
```

This will display the help information with available functions.

---

## Method 3: Import and use in other scripts

Create a script that imports `wifi_connect`:

```python
# my_app.py
import wifi_connect

# Scan networks
networks = wifi_connect.scan_networks()

# Connect to a network
ip = wifi_connect.connect_wifi('Your_SSID', 'your_password', timeout=15)

if ip:
    print(f"Connected with IP: {ip}")
    # Your code here...
else:
    print("Failed to connect!")

# Disconnect when done
wifi_connect.disconnect()
```

Then upload and run it:

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp my_app.py :my_app.py
mpremote connect /dev/cu.usbserial-0001 run my_app.py
```

---

## Function Reference

### `scan_networks()`

Scans for available WiFi networks and displays detailed information.

**Returns:** List of network tuples from `wlan.scan()`

**Example:**

```python
>>> networks = wifi_connect.scan_networks()
```

---

### `connect_wifi(ssid, password, timeout=10)`

Connects to a specified WiFi network with a configurable timeout.

**Parameters:**

- `ssid` (str): The WiFi network name
- `password` (str): The WiFi password
- `timeout` (int, optional): Maximum seconds to wait for connection (default: 10)

**Returns:** IP address (str) on success, or `None` on failure

**Example:**

```python
>>> ip = wifi_connect.connect_wifi('MyNetwork', 'MyPassword', timeout=15)
```

---

### `status()`

Displays the current WiFi connection status and IP address.

**Example:**

```python
>>> wifi_connect.status()
```

---

### `disconnect()`

Disconnects from the current WiFi network.

**Example:**

```python
>>> wifi_connect.disconnect()
```

---

## Troubleshooting

### Connection timeout

If you see "Connection timeout!", the network might be:

- Too far away (weak signal)
- Incorrect SSID or password
- Temporarily unavailable

Try increasing the timeout parameter:

```python
>>> wifi_connect.connect_wifi('SSID', 'password', timeout=30)
```

### "Not connected" message

Make sure you have successfully connected before calling `status()` or `disconnect()`.

### SSID or password not found

Use `scan_networks()` to verify the exact SSID and ensure the password is correct.

### No networks found

- Ensure your ESP32's antenna is not obstructed
- Move closer to the WiFi router
- Try `scan_networks()` again after a few seconds

---

## See also

- Check [README.md](README.md) for device setup and firmware flashing instructions
- Check [quick_connect.py.instruction.md](quick_connect.py.instruction.md) for simplified WiFi connection
