import socket
from typing import List, Dict
import numpy as np
from bt_proximity import BluetoothRSSI

vals = 10
port = 25022

class Gatherer:
    last_values: Dict[str, List] = {}

    def __init__(self, host_list):
        self.host_list = host_list

    def update_values(self, addr, new_val):
        if len(self.last_values[addr]) >= vals:
            self.last_values[addr].pop(0)
        self.last_values[addr].append(new_val)

    def bluetooth_listen(self, addr):
        b = BluetoothRSSI(addr=addr)
        rssi = b.request_rssi()
        if rssi:
            rssi = rssi[0]
            self.update_values(addr, rssi)

    def get_values(self):
        out = {}
        for addr in self.last_values:
            out[addr] = np.mean(self.last_values[addr])
        return out


class Server:
    def create_socket(self) -> socket.socket:
        """
        Creates the socket for the server.
        :param port:    port to be used to listen for clients
        :return:        server socket
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("127.0.0.1", port))
        server_socket.listen(5)
        return server_socket



