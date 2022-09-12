sudo apt-get install -y bridge-utils

sudo rm -f /etc/network/interfaces.d/eth0
sudo touch /etc/network/interfaces.d/eth0
echo "auto eth0
allow-hotplug eth0
iface eth0 inet manual
" | sudo tee -a /etc/network/interfaces.d/eth0

echo "denyinterfaces eth0" | sudo tee --append /etc/dhcpcd.conf
echo "denyinterfaces bat0" | sudo tee --append /etc/dhcpcd.conf


rm $(pwd)/start-batman-adv.sh
touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "#!/bin/bash
# batman-adv interface to use
sudo batctl if add wlan0
sudo ifconfig bat0 mtu 1468

sudo brctl addbr br0
sudo brctl addif br0 eth0 bat0

# Tell batman-adv this is a gateway client
sudo batctl gw_mode client

# Activates batman-adv interfaces
sudo ifconfig wlan0 up
sudo ifconfig bat0 up

# Restart DHCP now bridge and mesh network are up
sudo dhclient -r br0
sudo dhclient br0
" | tee -a $(pwd)/start-batman-adv.sh
