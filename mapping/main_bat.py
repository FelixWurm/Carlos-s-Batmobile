from get_batctl_data import createCSV
from graph_layout import getNodes
from drawer import drawNet
from graph_edges import setEdges
from name_mapper import mapNames

hosts = [
        "127.0.0.1",
        "192.168.199.1",
        "192.168.199.73",
        "192.168.199.21",
        "192.168.199.87",
        "192.168.199.60",
        "192.168.199.101",
        "192.168.199.102",
        "192.168.199.103",
        "192.168.199.104",
        "192.168.199.105",
        "192.168.199.106",
]


if __name__ == '__main__':
    while True:
        createCSV(hosts)
        nodes = getNodes()
        setEdges(nodes)
        mapNames(nodes)
        drawNet(nodes)