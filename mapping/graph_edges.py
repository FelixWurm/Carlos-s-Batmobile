import csv
import time

from drawer import Node


def findNodeWithName(nodes, name) -> Node:
    for node in nodes:
        if node.name == name:
            return node


def setEdges(nodes):
    with open("adjMat.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pinger = row['from/to']
            pingerN = findNodeWithName(nodes, pinger)
            for pingee in row:
                if pingee == "from/to":
                    continue

                try:
                    entry = int(row[pingee])
                except:
                    entry = 0
                if entry:
                    pingeeN = findNodeWithName(nodes, pingee)
                    if pingerN.pos in pingeeN.neighbors:
                        continue
                    pingerN.neighbors.append(pingeeN.pos)