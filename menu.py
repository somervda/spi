from board import SCL, SDA
import busio
import time
import RPi.GPIO as GPIO

# Set GPIO pins to read menu button values
PINUP=16
PINDOWN=20
PINSELECT=21
GPIO.setup(PINUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINSELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Import the SSD1306 module for OLED display on I2C.
import adafruit_ssd1306
# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# ssd1306 I2C device parameters
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
        # When the menu is first display it starts displaying from the firstItem in the itemList
        # and the initial window starts from the first item.
        self.selectedItemIndex = 0
        self.windowStartIndex=0
        selectedItem = None
        while selectedItem == None:
            selectedItem=self.processButtonPress()
            if selectedItem == None:
                if self.isI2C:
                    self.displayMenuOnI2c()
                else:
                    self.displayMenuOnTFT()
            else:
                return(selectedItem)
            time.sleep(0.1)

    def processButtonPress(self):
        # Check to see if the up, down or select buttons are pressed, if up or down then change the 
        # relavant selectedItemIndex and windowStartIndex values and redisplay the menu. If the select 
        # button is pressed then return the menuItem selected.
        if GPIO.input(PINUP)==0:
            if self.selectedItemIndex>0:
                self.selectedItemIndex-=1
                if self.selectedItemIndex<self.windowStartIndex:
                    self.windowStartIndex-=1
        if GPIO.input(PINDOWN)==0:
            print("Down")
            if self.selectedItemIndex<(len(self.itemList)-1):
                self.selectedItemIndex+=1
                if self.selectedItemIndex>=self.windowStartIndex+I2CWINDOWSIZE:
                    self.windowStartIndex+=1
        if GPIO.input(PINSELECT)==0:
            return(self.itemList[self.selectedItemIndex])
        return None


        
    def displayMenuOnTFT(self):
        print("displayMenuOnTFT is not implemented")

    def displaySelectionOnI2c(self,selectedItem):
        self.i2cDisplay.fill(0)
        self.i2cDisplay.text(selectedItem.name,0,0,1)
        self.i2cDisplay.show()
        time.sleep(3)
        self.i2cDisplay.fill(0)
        self.i2cDisplay.show()




    def displayMenuOnI2c(self):
        print("displayMenuOnI2c: ",self.selectedItemIndex,self.windowStartIndex)
        self.i2cDisplay.fill(0)
        for index,item in enumerate(self.itemList[self.windowStartIndex:],start=self.windowStartIndex):
            if index==self.selectedItemIndex:
                selectionIndicator="> "
            else:
                selectionIndicator="  "
            self.i2cDisplay.text(selectionIndicator +  item.name, 0, (index - self.windowStartIndex) * I2CFONTHEIGHT,1)
        self.i2cDisplay.show()





