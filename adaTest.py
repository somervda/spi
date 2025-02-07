import time
import busio
import digitalio
from board import SCK, MOSI, MISO, D18, D23
print("SCK:",SCK, " MOSI:", MOSI," MISO:", MISO," D18 DC:", D18, " D23 CS:",D23)

from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341


# Configuration for CS and DC pins:
CS_PIN = D23
DC_PIN = D18

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))




# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

# Create the ILI9341 display:
display = ili9341.ILI9341(spi, cs=digitalio.DigitalInOut(CS_PIN),
                          dc=digitalio.DigitalInOut(DC_PIN))

dump(display)

# Main loop:
while True:
    # Clear the display
    print("Draw Pixel")
    display.fill(0)
    # Draw a red pixel in the center.
    display.pixel(120, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)
    # Clear the screen blue.
    print("Clear")
    display.fill(color565(0, 0, 255))
    # Pause 2 seconds.
    time.sleep(2)