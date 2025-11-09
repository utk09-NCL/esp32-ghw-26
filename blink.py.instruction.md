# `blink.py` code output with instructions

This module demonstrates basic GPIO control by blinking the ESP32's onboard LED. It's a great first program to verify your MicroPython setup is working correctly.

## Prerequisites

- Your ESP32 must have MicroPython firmware installed (see [README.md](README.md))
- You must have `mpremote` installed (see [README.md](README.md))
- Your ESP32 must have an onboard LED connected to GPIO pin 2 (standard on most ESP32 boards)

## Understanding the code

The `blink.py` program:

1. Imports the `Pin` class to control GPIO pins
2. Creates a LED object on pin 2 configured as an output
3. Enters an infinite loop that:
   - Turns the LED on
   - Waits 1 second
   - Turns the LED off
   - Waits 1 second
4. Allows graceful exit via Ctrl+C

## Upload the `blink.py` file to your device

```bash
# Replace /dev/cu.usbserial-0001 with your device path
mpremote connect /dev/cu.usbserial-0001 fs cp blink.py :blink.py
```

---

## Method 1: Run the script directly

### Execute blink.py on your device

```bash
mpremote connect /dev/cu.usbserial-0001 run blink.py
```

### Expected output

```bash
Starting LED blink program...
LED is ON
LED is OFF
LED is ON
LED is OFF
LED is ON
LED is OFF
...
```

**What you should observe:**

- The onboard LED on your ESP32 will blink on and off every 1 second
- The console will print "LED is ON" and "LED is OFF" messages for each cycle

### Stop the program

Press `Ctrl+C` in the terminal:

```bash
LED is ON
LED is OFF
Program interrupted. Turning off LED.
```

---

## Method 2: Interactive usage via REPL

### Connect to the device REPL

```bash
mpremote connect /dev/cu.usbserial-0001 repl
```

### Expected connection message

```bash
# Connected to MicroPython at /dev/cu.usbserial-0001
# Use Ctrl-] or Ctrl-x to exit this shell

# raw REPL; CTRL-B to exit
# >
# MicroPython v1.26.1 on 2025-09-11; Generic ESP32 module with ESP32
# Type "help()" for more information.
```

### Manual LED blinking in REPL

Type the following commands line by line:

```python
>>> from machine import Pin
>>> import time
>>> led = Pin(2, Pin.OUT)
>>> print("Starting LED blink program...")
Starting LED blink program...
>>> while True:
...     led.on()
...     print("LED is ON")
...     time.sleep(1)
...     led.off()
...     print("LED is OFF")
...     time.sleep(1)
...
```

**Note:** After typing the loop, press `Enter` twice to start execution.

#### Expected output (continued)

```bash
LED is ON
LED is OFF
LED is ON
LED is OFF
LED is ON
LED is OFF
...
```

### Stop the loop

Press `Ctrl+C` to interrupt:

```python
KeyboardInterrupt
```

### Exit the REPL

Press `Ctrl+X` or `Ctrl+]` to exit

---

## Method 3: Use LED control in your own scripts

Create a custom blinking script:

```python
# my_blink.py
from machine import Pin
import time

led = Pin(2, Pin.OUT)

def blink(times=5, on_time=0.5, off_time=0.5):
    """Blink the LED a specified number of times"""
    for i in range(times):
        led.on()
        print(f"Blink {i+1}: ON")
        time.sleep(on_time)
        led.off()
        print(f"Blink {i+1}: OFF")
        time.sleep(off_time)
    print("Done blinking!")

# Blink the LED 10 times
blink(times=10, on_time=0.3, off_time=0.3)
```

Upload and run it:

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp my_blink.py :my_blink.py
mpremote connect /dev/cu.usbserial-0001 run my_blink.py
```

---

## Function Reference

### LED Control Methods

#### `led.on()`

Turns the LED on (sets pin to HIGH/1)

```python
>>> led.on()
```

#### `led.off()`

Turns the LED off (sets pin to LOW/0)

```python
>>> led.off()
```

#### `led.value(x)`

Sets the LED state directly (1 = on, 0 = off)

```python
>>> led.value(1)  # Turn on
>>> led.value(0)  # Turn off
```

#### `led.toggle()`

Toggles the LED state (on to off, off to on)

```python
>>> led.toggle()
```

---

## Customization examples

### Adjust blink speed

Modify the `time.sleep()` values in `blink.py`:

```python
time.sleep(0.5)   # Blink twice per second (faster)
time.sleep(2)     # Blink once every 2 seconds (slower)
```

### Different on/off times

```python
led.on()
print("LED is ON")
time.sleep(2)      # Stay on for 2 seconds

led.off()
print("LED is OFF")
time.sleep(0.5)    # Stay off for 0.5 seconds
```

### SOS morse code pattern

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

def dot():
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)

def dash():
    led.on()
    time.sleep(0.6)
    led.off()
    time.sleep(0.2)

# S-O-S pattern
for _ in range(3):
    dot()
    dot()
    dot()
    time.sleep(0.5)

    dash()
    dash()
    dash()
    time.sleep(0.5)

    dot()
    dot()
    dot()
    time.sleep(1)
```

---

## Troubleshooting

### LED doesn't blink

Check the following:

- **LED is plugged in:** Verify the LED is physically connected to pin 2
- **Power supply:** Ensure your ESP32 is powered on
- **Correct pin:** Some ESP32 variants may use a different pin for the onboard LED (try pins 4, 5, or 13)
- **Firmware installed:** Verify MicroPython is installed (see [README.md](README.md))

Try verifying with this test:

```python
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.on()
>>> # Does the LED turn on?
>>> led.off()
```

### Connection errors

If you see "failed to connect":

- Check the device path: `ls /dev/cu.*` on macOS/Linux
- Update the device path in commands if needed
- Try reconnecting the USB cable

### "KeyboardInterrupt" when trying to stop

This is normal. Press `Ctrl+C` again if needed, or use `Ctrl+D` to reset the REPL.

---

## Hardware reference

### GPIO Pin 2 on ESP32

- **Physical location:** Depends on ESP32 board variant
- **LED color:** Usually red
- **Current draw:** ~20 mA at 3.3V
- **Built-in resistor:** Most boards include current-limiting resistor

### Alternative pins for LED experiments

- Pin 4: Alternative GPIO
- Pin 5: Alternative GPIO
- Pin 13: Alternative GPIO (available on some boards)
- Pin 27, 33: Alternative GPIO

To use a different pin, change line 5 in `blink.py`:

```python
led = Pin(4, Pin.OUT)  # Use pin 4 instead
```

---

## See also

- Check [README.md](README.md) for device setup and firmware flashing instructions
- Check [wifi_connect.py.instruction.md](wifi_connect.py.instruction.md) for WiFi connectivity
- Check [quick_connect.py.instruction.md](quick_connect.py.instruction.md) for simplified WiFi setup
