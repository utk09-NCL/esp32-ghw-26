# ESP-32 (GHW API Week)

## Setup python virtual environment

```bash
python3 -m venv espenv # MacOS/Linux
python -m venv espenv  # Windows

source espenv/bin/activate # MacOS/Linux
.\espenv\Scripts\activate  # Windows

python -m pip install --upgrade pip # update pip
```

## Install dependencies

```bash
pip install esptool
pip install mpremote
```

## Install USB drivers (restart your system after installation)

- Windows/MacOS: [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)

- [AI generated] Linux: Usually no need to install drivers, as most distributions include them by default. Just make sure your user has permission to access serial devices (e.g., by adding your user to the `dialout` group).

## Check connection

```bash
ls /dev/cu.*  # MacOS/Linux
ls /dev/tty.* # Windows [AI generated]

# To identify the device, you can compare the list of devices before and after plugging in the ESP32:
# ls /dev/cu.* > before_esp.txt # List devices before plugging in ESP32
# ls /dev/cu.* > after_esp.txt # List devices after plugging in ESP32
# diff before_esp.txt after_esp.txt # Compare the two lists to find the new device
## > /dev/cu.SLAB_USBtoUART
## > /dev/cu.usbserial-0001 # Our ESP32 device
```

## Flash MicroPython firmware

### ⚠️ NOTE: Replace `/dev/cu.usbserial-0001` with your device path

```bash
# ⛔️ NOTE: This will erase all data on the device

esptool --chip esp32 --port /dev/cu.usbserial-0001 erase-flash

# Sample output:
# ❯ esptool --chip esp32 --port /dev/cu.usbserial-0001 erase-flash
# esptool v5.1.0
# Connected to ESP32 on /dev/cu.usbserial-0001:
# Chip type:          ESP32-D0WD-V3 (revision v3.1)
# Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
# Crystal frequency:  40MHz
# MAC:                6c:c8:40:89:e2:ac
# Stub flasher running.
# Flash memory erased successfully in 6.3 seconds.
# Hard resetting via RTS pin...
```

### ⚠️ NOTE: Download the latest firmware `.bin` file from [MicroPython ESP32 / WROOM Espressif](https://micropython.org/download/ESP32_GENERIC/)

```bash
### Replace the filename below with the one you downloaded
### In this example, we use ESP32_GENERIC-20250911-v1.26.1.bin
### replace --port value with your device path

esptool --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write-flash -z 0x1000 ESP32_GENERIC-20250911-v1.26.1.bin

# Sample output:
# ❯ esptool --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write-flash -z 0x1000 ESP32_GENERIC-20250911-v1.26.1.bin
# esptool v5.1.0
# Connected to ESP32 on /dev/cu.usbserial-0001:
# Chip type:          ESP32-D0WD-V3 (revision v3.1)
# Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
# Crystal frequency:  40MHz
# MAC:                6c:c8:40:89:e2:ac
# Stub flasher running.
# Changing baud rate to 460800...
# Changed.
# Configuring flash size...
# Flash will be erased from 0x00001000 to 0x001a8fff...
# Wrote 1734416 bytes (1137589 compressed) at 0x00001000 in 30.0 seconds (462.0 kbit/s).
# Hash of data verified.
# Hard resetting via RTS pin...
```

#### Explanation of the command

- `esptool` - The flashing tool.
- `--chip` esp32 - Target device is an ESP32.
- `--port /dev/cu.usbserial-0001` - Use this USB port to connect to the ESP32.
- `--baud 460800` - Use a fast transfer speed for flashing.
- `write-flash -z` 0x1000 - Write (upload) the firmware to memory address 0x1000 (standard for ESP32).
- `ESP32_GENERIC-20250911-v1.26.1.bin` - The firmware file to upload.

### Verify installation by connecting to the REPL

```bash
mpremote connect /dev/cu.usbserial-0001 repl
```

#### You should see the MicroPython REPL prompt

```python
>>> print("Hello from ESP32!")
# Hello from ESP32!

# Note: To exit the REPL, press Ctrl+] or Ctrl+X or Ctrl+C depending on your terminal.
# Sometimes, to reach the REPL, you may need to do CTRL+A, followed by CTRL+B

# Sample output:
# ❯ mpremote connect /dev/cu.usbserial-0001 repl
# Connected to MicroPython at /dev/cu.usbserial-0001
# Use Ctrl-] or Ctrl-x to exit this shell
# I pressed CTRL+A, got to
# raw REPL; CTRL-B to exit
# >
# I pressed CTRL+B, got to
# MicroPython v1.26.1 on 2025-09-11; Generic ESP32 module with ESP32
# Type "help()" for more information.
# >>> print("Hello from ESP32!")
# Hello from ESP32!
# >>>
# I pressed Ctrl+X to exit the REPL
```

## Check files on the device and read a file

```bash
mpremote connect /dev/cu.usbserial-0001 fs ls
# Sample output:
# ls :
#          139 boot.py

# print the content of a file on the device
mpremote connect /dev/cu.usbserial-0001 cat boot.py

# Sample output:
#   This file is executed on every boot (including wake-boot from deepsleep)
    #import esp
    #esp.osdebug(None)
    #import webrepl
    #webrepl.start()
```

## Upload a file to the device

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp filename.py :filename.py
```

## Upload a folder to the device

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp -r ./path/to/folder :
# This uploads all files from the local folder to the device's root directory

# To upload to a subdirectory on the device, specify the target path:
mpremote connect /dev/cu.usbserial-0001 fs cp -r ./path/to/folder :sub/dir/on/device
```

## Run the uploaded file

```bash
mpremote connect /dev/cu.usbserial-0001 run filename.py

# Alternate way to run the file:
mpremote connect /dev/cu.usbserial-0001 repl
>>> import filename
>>> filename.function_name()  # call specific function if needed

# Another way using exec:
mpremote connect /dev/cu.usbserial-0001 exec "import filename"

# or
mpremote connect /dev/cu.usbserial-0001 repl
>>> exec(open('filename.py').read())
```

## Delete a file from the device

```bash
mpremote connect /dev/cu.usbserial-0001 fs rm filename.py
```

## Reset the device

```bash
# The difference between `reset` and `soft reset`:
# - `reset`: Performs a hard reset, similar to pressing the reset button on the device.
# - `soft reset`: Performs a soft reset, which restarts the MicroPython interpreter without rebooting the entire device.

mpremote connect /dev/cu.usbserial-0001 repl
>>> import machine
>>> machine.reset()

>>> import machine
>>> machine.soft_reset()
```
