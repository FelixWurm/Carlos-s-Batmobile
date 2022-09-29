import os
import numpy as np

import ssh_tools
from ssh_tools import send


def spread(cmd):
    print(cmd)
    forks = 6
    hosts = []
    all_hosts = ssh_tools.get_host_list()
    all_hosts.append("192.168.199.1")
    all_hosts = np.array_split(all_hosts, forks)
    for i in range(forks):
        if not os.fork():
            forks = i + 1
            hosts = all_hosts[i]
            break
    else:
        while forks:
            os.wait()
            forks -= 1
        return
    if not len(hosts):
        exit(0)
    print("fork", forks, "- START - with", len(hosts), "hosts")
    for host in hosts:
        try:
            out = send(host, cmd)
            print(host.ljust(15), "-", out.strip())
        except KeyboardInterrupt:
            exit(0)
        except:
            pass
    exit(0)


cmd = [
    "sudo config wlan0 txpower 30",             # 0
    "sudo batctl hp",                           # 1
    "bluetoothctl discoverable on",             # 2
    "bluetoothctl discoverable-timeout 3600",   # 3
    "bluetoothctl list",                        # 4
    "sudo batctl gwl",                          # 5
    "hostname -I",                              # 6
    "sudo shutdown -r",                         # 7
    'sudo sed -i "s/wireless-channel 3/wireless-channel 36/" /etc/network/interfaces.d/wlan0',  # 8
    "sudo apt install -y iperf3"                # 9
]

if __name__ == '__main__':
    spread(cmd[8])
    spread(cmd[7])
