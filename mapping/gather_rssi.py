import math
import select
import socket
import time
from math import floor
from typing import List, Dict
import numpy as np
import json
import bt_names
from bt_proximity import BluetoothRSSI


MAX_VALS = 30

PORT = 25022

A_0 = 1
ENVIRONMENTAL_ERROR = 10
PATH_LOSS_EXPONENT = 1.5


def rssi_to_meter(rssi) -> float:
    return (math.pow(10, float((rssi - A_0) / (-10 * PATH_LOSS_EXPONENT))) * 100) + ENVIRONMENTAL_ERROR


class Gatherer:
    last_values: Dict[str, any] = {}


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


    def update_value(self, addr, new_val):
        if addr not in self.last_values:
            self.last_values[addr] = {}
            self.last_values[addr]["data"] = []
        if len(self.last_values[addr]["data"]) >= MAX_VALS:
            self.last_values[addr]["data"].pop(0)
        self.last_values[addr]["lastUpdate"] = floor(time.time())
        self.last_values[addr]["data"].append(new_val)


    def bluetooth_listen(self, addr):
        b = BluetoothRSSI(addr=addr)
        rssi = b.request_rssi()
        if rssi:
            rssi = rssi[0]
            # self.update_value(addr, rssi_to_meter(rssi))
            self.update_value(addr, rssi)


    def get_values(self) -> Dict[str, any]:
        out = {}
        for addr in self.last_values:
            out[addr] = {
                "lastUpdate": self.last_values[addr]["lastUpdate"],
                "valueCount": len(self.last_values[addr]["data"]),
                "mean": float(np.mean(self.last_values[addr]["data"])),
                "min": min(self.last_values[addr]["data"]),
                "max": max(self.last_values[addr]["data"])
            }
        return out


class Server:
    serv_sock: socket.socket
    conns: List[socket.socket] = []


    def create_socket(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv_sock.bind(("0.0.0.0", PORT))
        self.serv_sock.listen(5)
        self.conns.append(self.serv_sock)


    def check_for_request(self) -> (List[str], socket.socket):
        read_socks: List[socket.socket] = select.select(self.conns, [], [], 0)[0]
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
        sock.send(bytes(data, "utf-8"))
        sock.close()
        self.conns.remove(sock)


def main():
    try:
        server = Server()
        server.create_socket()

        gatherer = Gatherer(list(bt_names.name_map))

        while 1:
            gatherer.scan_next()

            if req := server.check_for_request():
                req, sock = req
                cmd, req = req[0], req[1:]

                if cmd == "getdata":
                    server.send_to_sock(sock, json.dumps(gatherer.get_values()))
                elif cmd == "hostlist":
                    pass
                elif cmd == "exit":
                    exit(0)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
