import time

import networkx as nx
import drawer
import csv
import scipy


def getNodes():
    G = nx.Graph()
    with open("rsiMat.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pinger = row['from/to']
            for pingee in row:
                if pingee == "from/to":
                    continue
                weight = row[pingee]
                if weight == '':
                    G.add_edge(pinger, pingee)
                else:
                    G.add_edge(pinger, pingee, weight=256 - max(.001, int(weight)))

    pos = nx.kamada_kawai_layout(G)


    def movPos(pos):
        return (pos[0] + 1) / 2, (pos[1] + 1) / 2


    nodes = []
    for n in pos:
        nodes.append(drawer.Node(movPos(pos[n]), n, 0))

    return nodes
