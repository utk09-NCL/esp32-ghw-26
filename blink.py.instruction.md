# `blink.py` code output with instructions

```bash
# connect to the device using mpremote
❯ mpremote connect /dev/cu.usbserial-0001 repl
# Connected to MicroPython at /dev/cu.usbserial-0001
# Use Ctrl-] or Ctrl-x to exit this shell

# raw REPL; CTRL-B to exit
# >
# MicroPython v1.26.1 on 2025-09-11; Generic ESP32 module with ESP32
# Type "help()" for more information.
```

```python
# start typing the following code in the REPL
>>> from machine import Pin
>>> import time
>>> led = Pin(2, Pin.OUT)
>>> print("Starting LED blink program...")
Starting LED blink program...
>>> while True:
...     led.value(1)
...     print("LED in ON")
...     time.sleep(0.5)
...     led.value(0)
...     print("LED is OFF")
...     time.sleep(0.5)
... # Press ENTER a couple of times to start the program
...
...
# Starts LED blinking with output:
LED in ON
LED is OFF
LED in ON
LED is OFF
...
# Notice the LED on the ESP32 board blinking ON and OFF every half second
```

## Check [README.md](README.md) for more details on how to upload `blink.py` to your device

### Run the `blink.py` file using `mpremote`

```bash
mpremote connect /dev/cu.usbserial-0001 run blink.py
```
