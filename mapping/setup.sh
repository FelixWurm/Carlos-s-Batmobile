sudo apt-get install -y bluetooth pi-bluetooth python3-pip bluez python-dev-is-python3 libbluetooth-dev pkg-config libboost-python-dev libboost-thread-dev libglib2.0-dev
pip install numpy pybluez bt-proximity

echo "
# bluetooth rssi mapping server
python /home/pi/Carlos-s-Batmobile/mapping/gather_rssi.py &
" | sudo tee -a start-batman-adv.sh
