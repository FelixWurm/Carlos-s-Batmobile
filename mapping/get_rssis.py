import csv
import json
import socket
import time

import bt_names
import ssh_tools


DATA_AGE = 60


def exit_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(b"exit")
    try:
        sock.recv(1024)
    except:
        exit(0)


def get_values_from(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(b"getdata")
    # sock.send(b"exit")
    return json.loads(sock.recv(1024).decode("utf-8"))


def filter_data(data):
    current_time = time.time()
    out = {"from/to": "server"}
    for addr in data:
        if current_time - data[addr]["lastUpdate"] <= DATA_AGE:
            out[addr] = data[addr]["mean"]
    return out


def filter_data_with_count(data):
    current_time = time.time()
    out = {"from/to": "server"}
    for addr in data:
        if current_time - data[addr]["lastUpdate"] <= DATA_AGE:
            out[addr] = str(data[addr]["valueCount"]) + "  " + str(data[addr]["mean"])
    return out


def filter_data_carlos_III(data):
    return data["B8:27:EB:D4:2A:88"]


def dict_to_csv(data):
    with open("rsiMat.csv", 'w') as cf:
        w = csv.DictWriter(cf, fieldnames=list(bt_names.name_map))
        w.writeheader()
        for dlist in data:
            w.writerow(dlist)


def main():
    while 1:
        time.sleep(2)
        print("-" * 20)
        data = []
        hosts = ssh_tools.get_host_list()
        hosts = ["192.168.199.103"]
        for host in hosts:
            try:
                values = get_values_from(host, 25022)
            except:
                continue
            if not values:
                continue
            data.append(filter_data_carlos_III(values))

        print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
    # exit_server("192.168.199.12", 25022)
