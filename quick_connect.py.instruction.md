# `quick_connect.py` code output with instructions

This module provides a simplified way to connect to WiFi on your ESP32. It uses predefined SSID and password for quick, one-command WiFi connection.

## Prerequisites

- Your ESP32 must have MicroPython firmware installed (see [README.md](README.md))
- You must have `wifi_connect.py` uploaded to your device (see [wifi_connect.py.instruction.md](wifi_connect.py.instruction.md))
- You must know your WiFi SSID (network name) and password

## Setup: Configure your WiFi credentials

Before uploading, edit `quick_connect.py` and replace the placeholder values:

```python
def quick_connect():
    SSID = "YOUR_WIFI_NAME"       # TODO: Replace with your WiFi SSID
    PASSWORD = "YOUR_PASSWORD"    # TODO: Replace with your WiFi password
    return connect_wifi(SSID, PASSWORD)
```

**Example after configuration:**

```python
def quick_connect():
    SSID = "HomeNetwork"          # Your actual WiFi network name
    PASSWORD = "MySecurePassword" # Your actual WiFi password
    return connect_wifi(SSID, PASSWORD)
```

## Upload files to your device

You need to upload both files for `quick_connect.py` to work:

```bash
# Replace /dev/cu.usbserial-0001 with your device path

# Upload wifi_connect.py (required dependency)
mpremote connect /dev/cu.usbserial-0001 fs cp wifi_connect.py :wifi_connect.py

# Upload quick_connect.py
mpremote connect /dev/cu.usbserial-0001 fs cp quick_connect.py :quick_connect.py
```

## Method 1: Run the script directly

```bash
mpremote connect /dev/cu.usbserial-0001 run quick_connect.py
```

### Sample output on success

```bash
Quick WiFi Connector
*************************
Attempting to connect using predefined SSID and PASSWORD...
Connecting to 'HomeNetwork'....
Connected!
  IP Address: 192.168.1.100
  Gateway:    192.168.1.1
  DNS:        8.8.8.8
Successfully connected! IP Address: 192.168.1.100
*************************
```

### Sample output on failure

```bash
Quick WiFi Connector
*************************
Attempting to connect using predefined SSID and PASSWORD...
Connecting to 'HomeNetwork'.
Connection timeout!
Failed to connect to WiFi.
*************************
```

---

## Method 2: Interactive usage via REPL

### Connect to the device REPL

```bash
mpremote connect /dev/cu.usbserial-0001 repl
```

### Connect using quick_connect

```python
>>> import quick_connect
>>> ip = quick_connect.quick_connect()
Connecting to 'HomeNetwork'....
Connected!
  IP Address: 192.168.1.100
  Gateway:    192.168.1.1
  DNS:        8.8.8.8
>>> print(f"Connected with IP: {ip}")
Connected with IP: 192.168.1.100
```

---

## Method 3: Use as a module in other scripts

Create a script that imports `quick_connect`:

```python
# my_app.py
import quick_connect

# Connect to WiFi using predefined credentials
ip = quick_connect.quick_connect()

if ip:
    print(f"WiFi connected! IP: {ip}")
    # Your application code here
else:
    print("WiFi connection failed!")
```

Then upload and run it:

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp my_app.py :my_app.py
mpremote connect /dev/cu.usbserial-0001 run my_app.py
```

---

## Function Reference

### `quick_connect()`

Connects to WiFi using predefined SSID and password from the module variables.

**Returns:** IP address (str) on success, or `None` on failure

**Example:**

```python
>>> import quick_connect
>>> ip = quick_connect.quick_connect()
```

---

## Troubleshooting

### Connection timeout

If you see "Connection timeout!", check:

- Your ESP32 is within range of the WiFi router
- The SSID and password in `quick_connect.py` are correct
- The WiFi network is available and broadcasting its SSID

### "Failed to connect to WiFi" message

This occurs when `quick_connect()` returns `None`. Verify:

- You've correctly configured the SSID and password in `quick_connect.py`
- You've re-uploaded the file after making changes: `mpremote connect /dev/cu.usbserial-0001 fs cp quick_connect.py :quick_connect.py`

### Module not found error

Make sure both files are uploaded:

```bash
mpremote connect /dev/cu.usbserial-0001 fs ls
```

You should see:

```bash
         ...
         ...
         1234 wifi_connect.py
         1234 quick_connect.py
```

If missing, upload them again (see [Upload files to your device](#upload-files-to-your-device) section).

### Incorrect credentials

If the SSID or password is wrong, use `wifi_connect` to scan networks and verify:

```python
>>> import wifi_connect
>>> wifi_connect.scan_networks()
```

Then update the credentials in `quick_connect.py` and re-upload.

---

## Difference between quick_connect.py and wifi_connect.py

| Feature | wifi_connect.py | quick_connect.py |
|---------|-----------------|------------------|
| **Purpose** | Full WiFi control module | Simple one-command WiFi connection |
| **Setup** | No configuration needed | Requires editing credentials |
| **Scan networks** | Yes (`scan_networks()`) | No |
| **Custom SSID/password** | Yes (pass as parameters) | No (use predefined) |
| **Connection control** | Full control | Auto-connect only |
| **Disconnect function** | Yes (`disconnect()`) | No |
| **Status function** | Yes (`status()`) | No |
| **Best for** | Development & testing | Quick deployment & automation |

---

## See also

- Check [README.md](README.md) for device setup and firmware flashing instructions
- Check [wifi_connect.py.instruction.md](wifi_connect.py.instruction.md) for full WiFi control documentation
