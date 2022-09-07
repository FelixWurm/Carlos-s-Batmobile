if [ $# -eq 0 ]
then
    BATINTERFACE="wlan0"
    GATEINTERFACE="eth0"
else
    BATINTERFACE=$1
    GATEINTERFACE=$2
fi

sudo apt install iptables dnsmasq


rm $(pwd)/start-batman-adv.sh
touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "
sudo batctl if add $BATINTERFACE

# Tell batman-adv this is an internet gateway
sudo batctl gw_mode server

# Set Gateway IP
ip addr add 1.0.0.1/24 broadcast 1.0.0.255 dev bat0

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o $GATEINTERFACE -j MASQUERADE
sudo iptables -A FORWARD -i $GATEINTERFACE -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o $GATEINTERFACE -j ACCEPT

# Activate interfaces
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up
" | tee -a $(pwd)/start-batman-adv.sh


sudo rm /etc/dnsmasq.conf
sudo touch /etc/dnsmasq.conf
echo "
# DHCP-Server active for the batman mesh network interface
interface=bat0

# DHCP-Server not active for internet network
no-dhcp-interface=$GATEINTERFACE

# IPv4-address range and lease-time
dhcp-range=1.0.0.50,1.0.0.150,24h

# DNS
dhcp-option=option:dns-server,8.8.8.8

# Gateway: needs to be the same as the ip of the bat0 interface in the startup script
dhcp-option=3,1.0.0.1
" | sudo tee -a  /etc/dnsmasq.conf

echo Installation done. Rebooting...
sleep 5
reboot
