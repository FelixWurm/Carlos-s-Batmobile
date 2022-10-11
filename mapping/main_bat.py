import time

import ssh_tools
from get_batctl_data import createCSV
from graph_layout import getNodes
from drawer import drawNet
from graph_edges import setEdges
from name_mapper import mapNames


hosts = ssh_tools.get_host_list()

if __name__ == '__main__':
    while True:
        createCSV(hosts)
        nodes = getNodes()
        setEdges(nodes)
        mapNames(nodes)
        drawNet(nodes)
