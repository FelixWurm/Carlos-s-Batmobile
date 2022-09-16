#!/bin/bash
#scribt to setup the IO part of the Project


#update the pi
apt-get update
apt-get upgrade


#install python libs
sudo apt install pip -y

#rtsp stuff
(cd /home/pi/Carlos-s-Batmobile/rtsp-server/; wget share.schwabauer.co/rtsp_server -O rtsp_server; chmod +x rtsp_server)


#install librarys for the camera
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3 libgstrtspserver-1.0-0 libgstrtspserver-1.0-dev -y
    
#echo "
#(cd /home/pi/Carlos-s-Batmobile/; git pull)
#python3 /home/pi/Carlos-s-Batmobile/controllsoftware/RPI_control.py
#" | sudo tee -a /home/pi/.bashrc

#hostnamectl set-hostname $1

#echo "
#sudo ifconfig bat0 $2
#" | sudo tee -a /home/pi/start-batman-adv.sh

