from machine import Pin
import time

# Initialize the built-in LED on GPIO pin 2
led = Pin(2, Pin.OUT)


def pattern_fast():
    """Fast blinking pattern"""
    print("Pattern: Fast blink")
    for _ in range(10):  # Loop 10 times
        led.on()
        time.sleep(0.1)  # 100ms on
        led.off()
        time.sleep(0.1)  # 100ms off


def pattern_slow():
    """Slow blinking pattern"""
    print("Pattern: Slow blink")
    for _ in range(3):  # Loop 3 times
        led.on()
        time.sleep(1)  # 1 second on
        led.off()
        time.sleep(1)  # 1 second off


def pattern_sos():
    """SOS distress signal in Morse code"""
    print("Pattern: SOS")

    # S: 3 short flashes (dots)
    for _ in range(3):
        led.on()
        time.sleep(0.2)  # Short flash
        led.off()
        time.sleep(0.2)

    time.sleep(0.5)  # Letter gap

    # O: 3 long flashes (dashes)
    for _ in range(3):
        led.on()
        time.sleep(0.6)  # Long flash
        led.off()
        time.sleep(0.2)

    time.sleep(0.5)  # Letter gap

    # S: 3 short flashes again
    for _ in range(3):
        led.on()
        time.sleep(0.2)  # Short flash
        led.off()
        time.sleep(0.2)


def pattern_heartbeat():
    """Heartbeat pattern"""
    print("Pattern: Heartbeat")
    for _ in range(5):  # Loop 5 times
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.7)  # Long pause for heartbeat effect


if __name__ == "__main__":
    print("\n" + "=" * 40)
    print("ESP32 LED PATTERN DEMO")
    print("=" * 40)
    print("Watch the LED for different patterns!")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            pattern_fast()
            time.sleep(2)

            pattern_slow()
            time.sleep(2)

            pattern_sos()
            time.sleep(2)

            pattern_heartbeat()
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nDemo stopped")
        led.off()  # Ensure LED is off on exit
