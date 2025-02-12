# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will draw a few rectangles onto the screen along with some text
on top of that.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
import time
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341
# from adafruit_rgb_display import st7789  # pylint: disable=unused-import
# from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
# from adafruit_rgb_display import st7735  # pylint: disable=unused-import
# from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
# from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 20

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
print("rotation:",disp.rotation % 180 )
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

print("Start Drawing")
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a green filled box as the background
draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)
# Load a TTF Font
font = ImageFont.truetype("ls /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
font_height=FONTSIZE
while True:
    start= time.time()
    # (font_width, font_height) = font.getsize(text)
    draw.text(
        (0, 0),
        "Menu",
        font=font,
        fill=(255, 255, 0),
    )
    draw.text(
        (0, font_height),
        "Planets",
        font=font,
        fill=(255, 255, 0),
    )
    draw.text(
        (0, font_height*2),
        "Satellites",
        font=font,
        fill=(255, 255, 0),
    )
    draw.text(
        (0, font_height*3),
        "Constellations",
        font=font,
        fill=(255, 255, 0),
    )
    draw.text(
        (0, font_height*4),
        "Setup",
        font=font,
        fill=(255, 255, 255),
    )

    # Display image.
    disp.image(image)
    print(time.time()-start)
    start = time.time()
    # Draw Some Text

    draw.text(
        (0, font_height*3),
        "Constellations",
        font=font,
        fill=(255, 255, 255),
    )
    draw.text(
        (0, font_height*4),
        "Setup",
        font=font,
        fill=(255, 255, 0),
    )

    # Display image.
    disp.image(image)
    print(time.time()-start)
