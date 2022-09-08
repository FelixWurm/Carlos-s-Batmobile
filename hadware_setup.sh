#!/bin/bash
#scribt to setup the IO part of the Project


#update the pi
apt-get update
apt-get upgrade


#install python pip
apt-get install pip


#install the importat python liberys
pip install smbus
pip install websockets
