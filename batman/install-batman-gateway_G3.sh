
BATINTERFACE="wlan0"
GATEINTERFACE="eth0"
NETIP=""

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
sudo batctl if add $BATINTERFACE
sudo batctl gw_mode server


# routing / internet access
sudo ip route add 169.254.0.0/16 dev bat0
# sudo route add -net 169.254.0.0/16 dev bat0

sudo sysctl -w net.ipv4.ip_forward=1

sudo iptables -t nat -A POSTROUTING ! -d 169.254.0.0/16 -o $GATEINTERFACE -j SNAT --to-source $NETIP
# sudo iptables -t nat -A POSTROUTING ! -d 169.254.0.0/16 -o $GATEINTERFACE -j MASQUERADE
sudo iptables -F
sudo iptables -t nat -F

#sudo iptables -t nat -A POSTROUTING -o $GATEINTERFACE -j MASQUERADE
#sudo iptables -A FORWARD -i $GATEINTERFACE -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
#sudo iptables -A FORWARD -i bat0 -o $GATEINTERFACE -j ACCEPT


# Activate interfaces
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up
sudo ifconfig bat0 $NETIP/16
" | tee -a $(pwd)/start-batman-adv.sh


sudo rm /etc/dnsmasq.conf
sudo touch /etc/dnsmasq.conf
echo "
interface=bat0
no-dhcp-interface=eth0
dhcp-range=169.254.3.5,169.3.254.254,254.254.0.0,infinite
" | sudo tee -a  /etc/dnsmasq.conf

echo Installation done. Rebooting...
sleep 5
reboot
