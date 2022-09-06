sudo apt install iptables


rm /home/pi/start-batman-adv.sh
touch /home/pi/start-batman-adv.sh
chmod +x /home/pi/start-batman-adv.sh
echo "
sudo batctl if add wlan0

# Tell batman-adv this is an internet gateway
sudo batctl gw_mode server

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o eth0 -j ACCEPT

# Activate interfaces
sudo ifconfig wlan0 up
sudo ifconfig bat0 up
" | tee -a /home/pi/start-batman-adv.sh
