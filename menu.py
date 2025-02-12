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
# import adafruit_ssd1306
# Create the I2C interface.
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

# i2c = busio.I2C(SCL, SDA)
ssdDisplay = i2c(port=1, address=0x3C)
# substitute ssd1331(...) or sh1106(...) below if using that device
# device = sh1106(serial)
ssd1309Device = ssd1309(ssdDisplay)
# See draw functions at https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#module-PIL.ImageDraw
# draw=canvas(ssd1309Device)


# ssd1306 I2C device parameters
I2CWIDTH=128
I2CHEIGHT=64
I2CWINDOWSIZE=7
I2CFONTHEIGHT=9

# SPI display setup
import digitalio
import board
import time
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341

FONTSIZE = 20
TFTWINDOWSIZE=10


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# disp = ili9341.ILI9341(
#     spi,
#     rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
#     cs=cs_pin,
#     dc=dc_pin,
#     rst=reset_pin,
#     baudrate=BAUDRATE,
# )





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
            self.background = Image.new(ssd1309Device.mode, ssd1309Device.size, "black")
            self.draw = ImageDraw.Draw(self.background)
            self.draw.text((0, 0), "Go Eagles", fill="white")
            ssd1309Device.display(self.background)
            # self.i2cDisplay = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, i2c)
        else:
            self.height = disp.width  # we swap height/width to rotate it to landscape!
            self.width = disp.height
            self.windowSize= TFTWINDOWSIZE
            # Make image and draw objects
            self.image = Image.new("RGB", (self.width, self.height))
            # Get drawing object to draw on image.
            self.draw = ImageDraw.Draw(self.image)
            # Load a TTF Font
            self.font = ImageFont.truetype("ls /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
            self.font_height=FONTSIZE

    

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
            # time.sleep(0.1)


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
                if self.selectedItemIndex>=self.windowStartIndex+self.windowSize:
                    self.windowStartIndex+=1
        if GPIO.input(PINSELECT)==0:
            return(self.itemList[self.selectedItemIndex])
        return None


        
    def displayMenuOnTFT(self):
        print("displayMenuOnTFT: ",self.selectedItemIndex,self.windowStartIndex)
        # Clear page
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
        # disp.image(self.image)
        for index,item in enumerate(self.itemList[self.windowStartIndex:],start=self.windowStartIndex):
            if index> (self.windowStartIndex + self.windowSize):
                break
            if index==self.selectedItemIndex:
                self.draw.text((0, (index - self.windowStartIndex) * (FONTSIZE +1)),item.name,font=self.font,fill=(255, 255, 255))
                # self.i2cDisplay.text(selectionIndicator +  item.name, 0, (index - self.windowStartIndex) * I2CFONTHEIGHT,1)
            else:
                self.draw.text((0, (index - self.windowStartIndex) * (FONTSIZE +1)),item.name,font=self.font,fill=(0, 255, 255))
        # Display image.
        disp.image(self.image)



    def displaySelectionOnI2c(self,selectedItem):
        print("selected:",selectedItem.name)
        self.draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")
        self.draw.text((0, 0), selectedItem.name, fill="white")
        ssd1309Device.display(self.background)
        time.sleep(3)



    def displaySelectionOnTFT(self,selectedItem):
        # Clear page
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
        disp.image(self.image)
        self.draw.text((0, 0),selectedItem.name,font=self.font,fill=(255, 255, 255))
        # Display image.
        disp.image(self.image)
        time.sleep(3)
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
        disp.image(self.image)



    def displayMenuOnI2c(self):
        print("displayMenuOnI2c: ",self.selectedItemIndex,self.windowStartIndex)
        # with canvas(ssd1309Device) as draw1:
        #     draw1.text((0, 0), "Hi", fill="white")
        #     time.sleep(1)
        # self.i2cDisplay.fill(0)
        self.draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")
        # with canvas(ssd1309Device) as draw1:
        # print(drawx,draw1)
        for index,item in enumerate(self.itemList[self.windowStartIndex:],start=self.windowStartIndex):
            if index==self.selectedItemIndex:
                selectionIndicator="> "
            else:
                selectionIndicator="  "
            self.draw.text((0, (index - self.windowStartIndex) * I2CFONTHEIGHT),selectionIndicator +  item.name, fill="white")
            # draw1.text((0, 0), "Hi", fill="white")
            # self.i2cDisplay.text(selectionIndicator +  item.name, 0, (index - self.windowStartIndex) * I2CFONTHEIGHT,1)
        # self.i2cDisplay.show()
        ssd1309Device.display(self.background)





