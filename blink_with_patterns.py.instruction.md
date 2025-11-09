# `blink_with_patterns.py` code output with instructions

This module demonstrates various LED blinking patterns on your ESP32. It showcases timing concepts, pattern logic, and creative ways to control GPIO pins using loops and delays.

## Prerequisites

- Your ESP32 must have MicroPython firmware installed (see [README.md](README.md))
- You must have `mpremote` installed (see [README.md](README.md))
- Your ESP32 must have an onboard LED connected to GPIO pin 2

## Understanding the code

The `blink_with_patterns.py` program includes four different LED pattern functions:

1. **`pattern_fast()`** - Rapid blinking (10 cycles of 0.1s each)
2. **`pattern_slow()`** - Slower blinking (3 cycles of 1s each)
3. **`pattern_sos()`** - Morse code SOS distress signal
4. **`pattern_heartbeat()`** - Heartbeat rhythm simulation

The main loop cycles through all patterns repeatedly, with 2-second pauses between each pattern.

## Upload the `blink_with_patterns.py` file to your device

```bash
# Replace /dev/cu.usbserial-0001 with your device path
mpremote connect /dev/cu.usbserial-0001 fs cp blink_with_patterns.py :blink_with_patterns.py
```

---

## Method 1: Run the script directly

### Execute blink_with_patterns.py on your device

```bash
mpremote connect /dev/cu.usbserial-0001 run blink_with_patterns.py
```

### Expected output

```bash
========================================
ESP32 LED PATTERN DEMO
========================================
Watch the LED for different patterns!
Press Ctrl+C to stop

Pattern: Fast blink
Pattern: Slow blink
Pattern: SOS
Pattern: Heartbeat
Pattern: Fast blink
Pattern: Slow blink
...
```

**What you should observe:**

- The onboard LED cycles through four distinct patterns
- Each pattern runs for 2-4 seconds before switching
- The console prints the current pattern name
- The cycle repeats continuously

### Stop the program

Press `Ctrl+C` in the terminal:

```bash
Pattern: Heartbeat
^C
Demo stopped
```

---

## Method 2: Interactive usage via REPL

### Connect to the device REPL

```bash
mpremote connect /dev/cu.usbserial-0001 repl
```

### Import the module

```python
>>> import blink_with_patterns
```

### Run individual patterns

```python
# Fast blinking
>>> blink_with_patterns.pattern_fast()
Pattern: Fast blink

# Slow blinking
>>> blink_with_patterns.pattern_slow()
Pattern: Slow blink

# SOS Morse code
>>> blink_with_patterns.pattern_sos()
Pattern: SOS

# Heartbeat rhythm
>>> blink_with_patterns.pattern_heartbeat()
Pattern: Heartbeat
```

### Create a custom pattern sequence

```python
>>> from machine import Pin
>>> import time
>>> led = Pin(2, Pin.OUT)
>>>
>>> # Run fast pattern twice
>>> blink_with_patterns.pattern_fast()
>>> time.sleep(1)
>>> blink_with_patterns.pattern_fast()
>>>
>>> # Run SOS
>>> blink_with_patterns.pattern_sos()
>>>
>>> # Run heartbeat 3 times
>>> for _ in range(3):
...     blink_with_patterns.pattern_heartbeat()
...     time.sleep(1)
...
```

### Exit the REPL

Press `Ctrl+X` or `Ctrl+]` to exit

---

## Method 3: Use patterns in your own scripts

Create a custom LED application:

```python
# light_show.py
import blink_with_patterns
import time

# Run specific patterns in custom order
patterns = [
    blink_with_patterns.pattern_heartbeat,
    blink_with_patterns.pattern_sos,
    blink_with_patterns.pattern_fast,
]

# Repeat 3 times
for cycle in range(3):
    print(f"\nCycle {cycle + 1}:")
    for pattern in patterns:
        pattern()
        time.sleep(1)

print("Light show complete!")
```

Upload and run:

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp light_show.py :light_show.py
mpremote connect /dev/cu.usbserial-0001 run light_show.py
```

---

## Pattern details

### Fast Blink

**Timing:** 10 cycles of 0.1s on / 0.1s off = 2 seconds total

**Visual effect:** Rapid, attention-getting

**Use cases:** Alerts, warnings, status indicators

```bash
|█ █ █ █ █ █ █ █ █ █|  (█ = on, space = off)
```

---

### Slow Blink

**Timing:** 3 cycles of 1s on / 1s off = 6 seconds total

**Visual effect:** Steady, easy to observe

**Use cases:** Activity indication, normal operation

```bash
|█         █         █         |
```

---

### SOS (Morse Code)

**Timing:** S (3×0.2s) + gap (0.5s) + O (3×0.6s) + gap (0.5s) + S (3×0.2s) ≈ 5 seconds total

**Morse code:**

- S = · · · (dot-dot-dot, short flashes)
- O = − − − (dash-dash-dash, long flashes)

**Visual effect:** Recognizable distress signal

**Use cases:** Emergency mode, critical alerts

```bash
|█ █ █|  pause  |███ ███ ███|  pause  |█ █ █|
```

---

### Heartbeat

**Timing:** Double pulse repeated 5 times with 0.7s pause = 4.5 seconds total

**Visual effect:** Mimics human heartbeat rhythm (lub-dub sound)

**Use cases:** Wellness monitoring, life detection, artistic effect

```bash
|█ █     █ █     █ █     █ █     █ █|
```

---

## Customization examples

### Create your own pattern

```python
def pattern_morse_hello():
    """Spell 'HELLO' in Morse code"""
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

    # H = ....
    for _ in range(4):
        dot()
    time.sleep(0.5)

    # E = .
    dot()
    time.sleep(0.5)

    # L = .-..
    dash()
    dot()
    dot()
    dot()
    time.sleep(0.5)

    # ... continue for L and O
```

### Adjust timing globally

Modify all patterns by changing the sleep durations:

```python
# Make everything faster (divide by 2)
time.sleep(0.05)  # Was 0.1
time.sleep(0.5)   # Was 1
time.sleep(0.1)   # Was 0.2
time.sleep(0.3)   # Was 0.6

# Make everything slower (multiply by 2)
time.sleep(0.2)   # Was 0.1
time.sleep(2)     # Was 1
time.sleep(0.4)   # Was 0.2
time.sleep(1.2)   # Was 0.6
```

### Random pattern selector

```python
from machine import Pin
import time
import random

led = Pin(2, Pin.OUT)

def random_pattern_demo():
    """Pick a random pattern each time"""
    patterns = [
        blink_with_patterns.pattern_fast,
        blink_with_patterns.pattern_slow,
        blink_with_patterns.pattern_sos,
        blink_with_patterns.pattern_heartbeat,
    ]

    for _ in range(10):
        random_pattern = random.choice(patterns)
        random_pattern()
        time.sleep(1)
```

---

## Troubleshooting

### LED doesn't blink

Check the following:

- **Verify the module loads:** `import blink_with_patterns`
- **Test basic LED control:** Use `blink.py` to verify LED works
- **Check GPIO pin:** Try different pins (4, 5, 13) if pin 2 doesn't work
- **Verify upload:** `mpremote connect /dev/cu.usbserial-0001 fs ls`

### Patterns run too fast or too slow

Adjust the `time.sleep()` values in each pattern function:

- Decrease values for faster patterns (e.g., 0.05 instead of 0.1)
- Increase values for slower patterns (e.g., 0.5 instead of 0.2)

### Can't import the module

Make sure the file is uploaded:

```bash
mpremote connect /dev/cu.usbserial-0001 fs ls
# Should see: blink_with_patterns.py
```

If not, upload it again:

```bash
mpremote connect /dev/cu.usbserial-0001 fs cp blink_with_patterns.py :blink_with_patterns.py
```

### Patterns interrupt each other

The main program cycles through all patterns. To run a specific pattern:

1. Use Method 2 (REPL) to call individual pattern functions
2. Create a custom script (Method 3) with your desired pattern sequence

---

## Learning concepts demonstrated

This module teaches several important programming concepts:

### Timing and Delays

- Using `time.sleep()` for precise timing control
- Creating patterns with different durations

### Functions and Abstraction

- Organizing code into reusable functions
- Each pattern is a self-contained function

### Loops

- `for` loops for repetitive tasks
- Infinite `while` loops for continuous execution

### GPIO Control

- Setting pin HIGH (on) and LOW (off)
- Hardware timing constraints

### Pattern Logic

- Morse code timing and structure
- Creative use of timing to simulate real-world effects (heartbeat)

### Exception Handling

- Using `try/except` for graceful shutdown
- Cleanup operations (`led.off()`)

---

## Hardware reference

### GPIO Pin 2

- Standard LED pin on most ESP32 boards
- Built-in current-limiting resistor (usually included)
- Sufficient current for LED brightness

### Alternative pins for experimentation

Try different GPIO pins by modifying line 4:

```python
led = Pin(4, Pin.OUT)   # Pin 4
led = Pin(5, Pin.OUT)   # Pin 5
led = Pin(13, Pin.OUT)  # Pin 13 (some boards)
```

---

## See also

- Check [README.md](README.md) for device setup and firmware flashing
- Check [blink.py.instruction.md](blink.py.instruction.md) for basic LED control
- Check [wifi_connect.py.instruction.md](wifi_connect.py.instruction.md) for WiFi connectivity
