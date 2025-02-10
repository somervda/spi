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

    def showMenu(self,startAtItem=0):
        # display menu on the selected device
        # When the menu is first display it starts displaying from the firstItem in the itemList
        # and the initial window starts from the first item.
        self.selectedItemIndex = 0
        self.windowStartIndex=0
        if self.isI2C:
            self.displayMenuOnI2c(startAtItem)
        else:
            self.displayMenuOnTFT(startAtItem)

    def processButtonPress():
        # Check to see if the up, down or select buttons are pressed, if up or down then change the 
        # relavant selectedItemIndex and windowStartIndex values and redisplay the menu. If the select 
        # button is pressed then return the menuItem selected.
        
    def displayMenuOnTFT(self):
        print("displayMenuOnTFT is not implemented")

    def displayMenuOnI2c(self,startAtItem):
        self.i2cDisplay.fill(0)
        for index,item in enumerate(self.itemList[startAtItem:],start=startAtItem):
            if index==self.selectedItemIndex:
                selectionIndicator="> "
            else:
                selectionIndicator="  "
            self.i2cDisplay.text(selectionIndicator +  item.name, 0, index * I2CFONTHEIGHT,1)
        self.i2cDisplay.show()





