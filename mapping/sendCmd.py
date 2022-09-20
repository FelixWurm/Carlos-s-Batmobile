import os
import numpy as np

import ssh_tools
from ssh_tools import send

#

cmd = [
    "sudo config wlan0 txpower 30",
    "sudo batctl hp",
    "bluetoothctl discoverable on",
    "sudo batctl gwl",
    "hostname -I",
]


if __name__ == '__main__':
    cmd = cmd[2]
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

