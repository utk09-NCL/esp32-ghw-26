# Import Pin class to control GPIO pins, already available in MicroPython
from machine import Pin
import time

# most ESP32 boards have an onboard LED connected to pin 2
led = Pin(2, Pin.OUT)

print("Starting LED blink program...")

try:
    while True:
        led.on()  # Alternative way to turn LED on
        print("LED is ON")
        time.sleep(1)  # Wait for 1 second

        led.off()  # Alternative way to turn LED off
        print("LED is OFF")
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:  # Allow graceful exit on Ctrl+C
    print("Program interrupted. Turning off LED.")
    led.off()  # Ensure LED is turned off on exit
