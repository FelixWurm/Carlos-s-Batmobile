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

git clone https://github.com/FelixWurm/Carlos-s-Batmobile.git


# Have batman-adv startup automatically on boot
echo "batman-adv" | sudo tee --append /etc/modules

# Prevent DHCPCD from automatically configuring $BATINTERFACE
echo "denyinterfaces $BATINTERFACE" | sudo tee --append /etc/dhcpcd.conf

sudo rm -f /etc/network/interfaces.d/bat0
sudo touch /etc/network/interfaces.d/bat0
echo "auto bat0
iface bat0 inet auto
    pre-up /usr/sbin/batctl if add $BATINTERFACE" | sudo tee -a /etc/network/interfaces.d/bat0

sudo rm -f /etc/network/interfaces.d/$BATINTERFACE
sudo touch /etc/network/interfaces.d/$BATINTERFACE
echo "auto $BATINTERFACE
iface $BATINTERFACE inet manual
    mtu 1532
    wireless-channel 3
    wireless-essid BatNet
    wireless-mode ad-hoc
    wireless-ap 02:12:34:56:78:9A" | sudo tee -a /etc/network/interfaces.d/$BATINTERFACE
    

rm -f $(pwd)/start-batman-adv.sh
touch $(pwd)/start-batman-adv.sh
chmod +x $(pwd)/start-batman-adv.sh
echo "
sudo batctl if add $BATINTERFACE
sudo batctl gw_mode client
sudo ifconfig $BATINTERFACE up
sudo ifconfig bat0 up
" | tee -a $(pwd)/start-batman-adv.sh

rm -f ~/connect-to-gateway.sh
touch ~/connect-to-gateway.sh
echo "
sudo rm -f /etc/resolv.conf
sudo touch /etc/resolv.conf
echo '
nameserver 1.1.1.1
nameserver 8.8.8.8
' | sudo tee -a /etc/resolv.conf
sudo ip route delete default
sudo ip route add default via 169.254.1.1 dev bat0
" | tee -a ~/connect-to-gateway.sh

rm -f ~/watchBat.sh
touch ~/watchBat.sh
chmod +x ~/watchBat.sh
echo "watch -n .1 'sudo batctl gwl;echo;echo;echo;sudo batctl o | grep -ie BATMAN -ie last-seen -ie \*'" | tee -a ~/watchBat.sh


# Enable interfaces on boot
echo "$(pwd)/start-batman-adv.sh" >> ~/.bashrc

echo Installation done. Rebooting...
sleep 5
reboot
