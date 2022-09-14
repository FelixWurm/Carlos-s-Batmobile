#!/bin/bash
#scribt to setup the IO part of the Project


#update the pi
apt-get update
apt-get upgrade


#install librarys for the camera
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3 libgstrtspserver-1.0-0 libgstrtspserver-1.0-dev

echo "
(cd /home/pi/Carlos-s-Batmobile/; git pull)
python3 /home/pi/Carlos-s-Batmobile/controllsoftware/RPI_control.py
" | sudo tee -a /home/pi/.bashrc
