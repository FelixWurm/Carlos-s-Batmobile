import select
import socket
from typing import List, Dict
import numpy as np
from bt_proximity import BluetoothRSSI
import json
import bt_names

vals = 10
port = 25022


class Gatherer:
    last_values: Dict[str, List] = {}


    def __init__(self, host_list):
        self.host_list = host_list
        self.last_index = 0


    def scan_next(self):
        if not self.host_list:
            return
        self.last_index += 1
        if self.last_index >= len(self.host_list):
            self.last_index = 0
        self.bluetooth_listen(self.host_list[self.last_index])


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


    def get_values(self) -> Dict[str, float]:
        out = {}
        for addr in self.last_values:
            out[addr] = float(np.mean(self.last_values[addr]))
        return out


class Server:
    serv_sock: socket.socket
    conns: List[socket.socket]


    def create_socket(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv_sock.bind(("127.0.0.1", port))
        self.serv_sock.listen(5)
        self.conns.append(self.serv_sock)


    def check_for_request(self) -> (List[str], socket.socket):
        read_socks: List[socket.socket] = select.select(self.conns, [], [])[0]
        for sock in read_socks:
            if sock == self.serv_sock:
                sockfd, addr = self.serv_sock.accept()
                self.conns.append(sockfd)
            else:
                data = sock.recv(1024)
                if data:
                    return data.decode("utf-8").split("|"), sock
        return ""


    def send_to_sock(self, sock: socket.socket, data: str):
        sock.send(bytes(data))
        sock.close()
        self.conns.remove(sock)


def main():
    server = Server()
    server.create_socket()

    gatherer = Gatherer(bt_names.name_map.keys())

    while 1:
        gatherer.scan_next()

        if req := server.check_for_request():
            req, sock = req
            cmd = req[0]
            req = req[1:]

            if cmd == "getdata":
                server.send_to_sock(sock, json.dumps(gatherer.get_values()))
            elif cmd == "hostlist":
                pass
            elif cmd == "stop":
                exit(0)


if __name__ == '__main__':
    main()