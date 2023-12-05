sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel


import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 64  # Number of LED pixels
LED_PIN = 40  # GPIO pin connected to the pixels (using BCM numbering)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def glow():
    global strip

    # Glow effect parameters
    speed = 10  # Adjust speed of the glow effect
    max_brightness = 255

    for i in range(LED_COUNT):
        # Calculate brightness based on a sine wave
        brightness = int((max_brightness / 2) * (1 + (1.0 * (1 + i)) / LED_COUNT))
        strip.setPixelColor(i, Color(brightness, brightness, brightness))

    strip.show()
    time.sleep(1.0 / speed)

try:
    while True:
        glow()

except KeyboardInterrupt:
    # Ctrl+C will exit the program
    strip.clear()
    strip.show()
