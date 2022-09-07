if [ $# -eq 0 ]
then
    BATINTERFACE="wlan0"
else
    BATINTERFACE=$1
fi


sudo rfkill unblock all
sudo apt update
sudo apt upgrade -y
sudo apt install -y libnl-3-dev libnl-genl-3-dev batctl alfred nmap git


# Have batman-adv startup automatically on boot
echo "batman-adv" | sudo tee --append /etc/modules

# Prevent DHCPCD from automatically configuring $BATINTERFACE
echo 'denyinterfaces $BATINTERFACE' | sudo tee --append /etc/dhcpcd.conf


sudo touch /etc/network/interfaces.d/bat0
echo "auto bat0
iface bat0 inet auto
    pre-up /usr/sbin/batctl if add $BATINTERFACE" | sudo tee -a /etc/network/interfaces.d/bat0

sudo touch /etc/network/interfaces.d/$BATINTERFACE
echo "auto $BATINTERFACE
iface $BATINTERFACE inet manual
    mtu 1532
    wireless-channel 3
    wireless-essid BatNet
    wireless-mode ad-hoc
    wireless-ap 02:12:34:56:78:9A" | sudo tee -a /etc/network/interfaces.d/$BATINTERFACE
    

touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "
sudo batctl if add $BATINTERFACE
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up" | tee -a $(pwd)/start-batman-adv.sh

touch ~/watchBat.sh
chmod +x ~/watchBat.sh
echo "watch -n .1 'sudo batctl o;echo;echo;echo;echo;echo;sudo batctl n'" | tee -a ~/watchBat.sh


# Enable interfaces on boot
echo "$(pwd)/start-batman-adv.sh" >> ~/.bashrc

echo Installation done. Rebooting...
sleep 5
reboot
