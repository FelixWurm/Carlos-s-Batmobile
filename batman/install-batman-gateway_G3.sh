
BATINTERFACE="wlan0"
GATEINTERFACE="eth0"
NETIP="192.168.199.1"

while getopts b:g:n: flag
do
    case "${flag}" in
        b) BATINTERFACE=${OPTARG};;
        g) GATEINTERFACE=${OPTARG};;
        n) NETIP=${OPTARG};;
    esac
done

if [ -z $NETIP ]
then
    echo "
        -b BATINTERFACE     optional
        -g GATEINTERFACE    optional
        -n NETIP            required
        "
    return 0
fi

sudo apt install iptables dnsmasq -y


rm $(pwd)/start-batman-adv.sh
touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "
#!/bin/bash
# batman-adv interface to use
sudo batctl if add $BATINTERFACE
sudo ifconfig bat0 mtu 1468

# Tell batman-adv this is an internet gateway
sudo batctl gw_mode server

# Enable port forwarding
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o $GATEINTERFACE -j MASQUERADE
sudo iptables -A FORWARD -i $GATEINTERFACE -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o $GATEINTERFACE -j ACCEPT

# Activates batman-adv interfaces
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up
sudo ifconfig bat0 $NETIP/24
" | tee -a $(pwd)/start-batman-adv.sh


sudo rm /etc/dnsmasq.conf
sudo touch /etc/dnsmasq.conf
echo "
interface=bat0
no-dhcp-interface=eth0
dhcp-range=192.168.199.2,192.168.199.99,255.255.255.0,12h
" | sudo tee -a  /etc/dnsmasq.conf

echo Installation done. Rebooting...
sleep 5
reboot
