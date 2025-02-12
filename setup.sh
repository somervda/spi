# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name "iot"
# git config --global user.email ""

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Installing and rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python3-pip
sudo apt install -y python-dev-is-python3

python --version
pip --version

sudo apt-get -y install python3-pil

# numpy speeds up the rgb display 
pip install numpy --break-system-packages

pip install adafruit-circuitpython-rgb-display --break-system-packages

echo 3. Installing OPi.GPIO 
# Install GPIO support for the orange PI 
# see https://pypi.org/project/RPi.GPIO/ and https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ 
# Note: Use GPIO.setmode(GPIO.SUNXI) to use "PA01" style channel naming
pip install RPi.GPIO --break-system-packages
# Enable i2c hardware
sudo raspi-config nonint do_i2c 0


echo 4. Installing python i2c and oled support
# Adafruit version (Circuit python and python)
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/main 
# Use i2cdetect to make sure you see the i2c device on the I2C 1 bus (Pins 3 and 5)  
# i2cdetect -y 1
echo 4a. Install i2c utilities
#  Can run i2c scans i.e. 'i2cdetect -y 1'
sudo apt-get install -y i2c-tools
# Give pi user access to i2c
sudo usermod -a -G spi,gpio,i2c pi
echo 4b. OLED Installing adafruit i2c and oled support
pip3 install adafruit-circuitpython-ssd1306 --break-system-packages
# Install luma oled libraries
pip install --upgrade luma.oled  --break-system-packages