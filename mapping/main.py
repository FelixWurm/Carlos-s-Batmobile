from get_batctl_data import createCSV
from graph_layout import getNodes
from drawer import drawNet
from graph_edges import setEdges

hosts = [
        "127.0.0.1",
        "192.168.199.1",
        "192.168.199.45",
        "192.168.199.123",
        #"192.168.199.104",
        #"192.168.199.105",
]


if __name__ == '__main__':
    while True:
        createCSV(hosts)
        nodes = getNodes()
        setEdges(nodes)
        drawNet(nodes)