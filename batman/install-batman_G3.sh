if [ $# -eq 0 ]
then
    BATINTERFACE="wlan0"
else
    BATINTERFACE=$1
fi
cd ~/


sudo rfkill unblock all
sudo apt update
sudo apt upgrade -y
sudo apt install -y libnl-3-dev libnl-genl-3-dev batctl alfred nmap git

git clone https://github.com/FelixWurm/Carlos-s-Batmobile.git


# Have batman-adv startup automatically on boot
echo "batman-adv" | sudo tee --append /etc/modules

# Prevent DHCPCD from automatically configuring $BATINTERFACE
echo "denyinterfaces $BATINTERFACE" | sudo tee --append /etc/dhcpcd.conf


sudo rm -f /etc/network/interfaces.d/$BATINTERFACE
sudo touch /etc/network/interfaces.d/$BATINTERFACE
echo "auto $BATINTERFACE
iface $BATINTERFACE inet manual
    wireless-channel 3
    wireless-essid BatNetG3
    wireless-mode ad-hoc
" | sudo tee -a /etc/network/interfaces.d/$BATINTERFACE
    

rm -f $(pwd)/start-batman-adv.sh
touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "
sudo batctl if add $BATINTERFACE
sudo ifconfig bat0 mtu 1468
sudo batctl gw_mode client
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up
# sudo iw $BATINTERFACE set power_save off
" | tee -a $(pwd)/start-batman-adv.sh


sudo sed -i 's/exit 0/\/home\/pi\/start-batman-adv.sh\nexit 0/' /etc/rc.local
echo Installation done. Rebooting...
sleep 5
reboot
