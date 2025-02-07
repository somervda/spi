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

pip3 install adafruit-circuitpython-rgb-display --break-system-packages