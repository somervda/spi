from board import SCL, SDA
import busio
import time
# Import the SSD1306 module for OLED display on I2C.
import adafruit_ssd1306
# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)



I2CWIDTH=128
I2CHEIGHT=64
I2CWINDOWSIZE=7
I2CFONTHEIGHT=9


class MenuItem():
    def __init__(self,name, description, elevation, bearing, distance, brightness):
        self.name = name
        self.description = description
        self.elevation=elevation
        self.bearing=bearing
        self.distance=distance
        self.brightness = brightness


class Menu:
    def __init__(self,isI2C,itemList):
        # Note: ssd1306 displays normally have a height=64 and wifdth-128
        self.itemList = itemList
        self.isI2C = isI2C
        if isI2C:
            self.height = I2CHEIGHT
            self.width = I2CWIDTH
            self.windowSize = I2CWINDOWSIZE
            self.i2cDisplay = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, i2c)

    def showMenu(self):
        # display menu on the selected device
        if self.isI2C:
            self.displayMenuOnI2c()
        else:
            self.displayMenuOnTFT()
        
    def displayMenuOnTFT(self):
        print("displayMenuOnTFT is not implemented")

    def displayMenuOnI2c(self):
        self.i2cDisplay.fill(0)
        self.i2cDisplay.show()
        for i,item in enumerate(self.itemList):
            self.i2cDisplay.text("  " + str(i+1) + " " + item.name, 0, i * I2CFONTHEIGHT,1)
        self.i2cDisplay.show()





