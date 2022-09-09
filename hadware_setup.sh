#!/bin/bash
#scribt to setup the IO part of the Project


#update the pi
apt-get update
apt-get upgrade


#install python pip
sudo apt-get install pip


#install the importat python liberys
pip install smbus
pip install websockets


echo "python3 /home/pi/Carlos-s-Batmobile/RPI_control.py" | sudo tee -a /home/pi/.bashrc
