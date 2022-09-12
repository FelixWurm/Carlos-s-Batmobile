sudo rm -f /etc/network/interfaces.d/bat0

sudo rm -f /etc/network/interfaces.d/wlan0
sudo touch /etc/network/interfaces.d/wlan0
echo "auto wlan0
iface wlan0 inet manual
    wireless-channel 3
    wireless-essid BatNet
    wireless-mode ad-hoc
" | sudo tee -a /etc/network/interfaces.d/wlan0


sudo sed -i "s/\/home\/pi\/start-batman-adv.sh/\n/" /home/pi/.bashrc



sudo rm -f /etc/rc.local
sudo touch /etc/rc.local
sudo chmod +x /etc/rc.local
echo "
#!/bin/sh -e
$(pwd)/start-batman-adv.sh
exit 0
" | sudo tee -a /etc/rc.local

echo Installation done. Rebooting...
sleep 5
reboot
