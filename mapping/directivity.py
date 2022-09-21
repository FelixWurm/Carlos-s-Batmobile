import math
import os
import select
import socket
import time
from math import floor
from os.path import exists
from typing import List, Dict
import numpy as np
import json
import bt_names
from bt_proximity import BluetoothRSSI

FILENAME = "directivity.csv"
ADDRESS = "B8:27:EB:4C:9A:27"
MAX_VAL_COUNT = 1000

def write_to_file(content):
    with open(FILENAME, "a") as f:
        f.write(content)


def write_header():
    write_to_file("distance,angle,rssi..." + os.linesep)


def add_value(val):
    write_to_file("," + str(val))


def bluetooth_listen(addr):
    b = BluetoothRSSI(addr=addr)
    rssi = b.request_rssi()
    if rssi:
        rssi = - rssi[0]
        return rssi
    return 0


def main():
    if not exists(FILENAME):
        write_header()

    distance = int(input("Distance >"))
    angle    = int(input("Angle    >"))
    val_count = 0

    write_to_file(str(distance) + "," + str(angle))


    try:
        while val_count < MAX_VAL_COUNT:
            time.sleep(.1)
            if rssi := bluetooth_listen(ADDRESS):
                add_value(rssi)
                val_count += 1
                print(str(val_count).ljust(10), rssi)
    except:
        pass
    write_to_file(os.linesep)


if __name__ == '__main__':
    main()