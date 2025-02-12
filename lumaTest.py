from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import time

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
# device = sh1106(serial)
device = ssd1309(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="black", fill="black")
    draw.text((0, 0), "  Planets", fill="white")
    draw.text((0, 9), "> Stars", fill="white")
    draw.text((0, 18), "  Constellations", fill="white")
    draw.text((0, 27), "  Satellites", fill="white")
time.sleep(10)