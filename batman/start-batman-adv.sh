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
sudo ifconfig bat0 169.254.1.1/16
