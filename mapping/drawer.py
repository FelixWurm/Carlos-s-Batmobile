import math
import os
import time

import terminedia as TM


def rectRot(pos, dim, rot: float = 0, erase=False):
    def rotP(p, rot, off=(0, 0)):
        # rotates a point (p) around (0,0) by rad (rot) and offsets it by off
        return round(p[0] * math.cos(rot) - p[1] * math.sin(rot) + off[0]), round(
            p[0] * math.sin(rot) + p[1] * math.cos(rot) + off[
                1])


    rot = rot % (2 * math.pi)
    w, h = dim

    # corners
    c1 = rotP((-w / 2, -h / 2), rot, pos)
    c2 = rotP((w / 2, -h / 2), rot, pos)
    c3 = rotP((w / 2, h / 2), rot, pos)
    c4 = rotP((-w / 2, h / 2), rot, pos)

    # draw lines
    sc.high.draw.line(c1, c2, erase=erase)
    sc.high.draw.line(c2, c3, erase=erase)
    sc.high.draw.line(c3, c4, erase=erase)
    sc.high.draw.line(c4, c1, erase=erase)


def drawNode(node):
    # rectRot(node.pos, (5,3), node.rot)
    # sc.high.draw.rect(node.pos, (node.pos[0] + 7, node.pos[1] + 4))
    sc.high.print_at((node.pos[0] - len(node.name), node.pos[1]), " ")
    sc.print(node.name, effects=TM.Effects.underline)


class Node:


    def __init__(self, pos, name, rot=0):
        self.rot = rot
        self.name = name
        self.pos = pos
        self.neighbors = []


def posMod(pos, scale):
    return math.floor(pos[0] * scale + 16), math.floor(pos[1] * scale + 5)


def drawNet(nodes):
    global sc
    # with TM.Screen() as sc:
    sc = TM.Screen()
    os.system("clear")
    scale = min(sc.size.x, sc.size.y) * 2 * .8
    for node in nodes:
        if ':' in node.name:
            node.name = node.name[9:]
        node.pos = posMod(node.pos, scale)
        for n in node.neighbors:
            n = posMod(n, scale)
            sc.high.draw.line(node.pos, n)
    for node in nodes:
        drawNode(node)
    sc.high.print_at((1, 1), " ")
