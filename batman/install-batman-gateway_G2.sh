
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
dhcp-range=169.254.3.5,169.254.3.254,12h
dhcp-option=option:router,$NETIP
dhcp-option=option:dns-server,192.168.1.1

dhcp-lease-max=1000
dhcp-rapid-commit
#dhcp-script /home/pi/Carlos-s-Batmobile/batman/dhcp-logger.sh

log-queries
log-dhcp

no-resolv
address=/gateway/169.254.0.0
dhcp-host=B2:3C:89:E1:D8:7A,spanier-ohne-auto-c # iwconfig cell
dhcp-host=b8:27:eb:c3:27:9b,spanier-ohne-auto-w # ifconfig wlan0
dhcp-host=3e:fa:da:13:fb:d5,spanier-ohne-auto-b # ifconfig bat0
" | sudo tee -a  /etc/dnsmasq.conf
chmod +x $(pwd)/Carlos-s-Batmobile/batman/dhcp-logger.sh

echo Installation done. Rebooting...
sleep 5
reboot
