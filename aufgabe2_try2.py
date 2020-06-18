from pptree import *
import numpy as np
import random
import itertools


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.ID = int(name[-1])
        self.send = None
        self.recv = None

        if parent:
            self.parent.children.append(self)

    def adj(self):
        c = []
        if self.parent is not None:
            c += [self.parent]
        c += self.children
        return c

    def __delitem__(self, key):
        self.__delattr__(self.ID)

    def __getitem__(self, item):
        return self.__getattribute__(self.item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        return self.name + other

    def __radd__(self, other):
        return other + self.name

    def __del__(self):
        pass


def setup():
    s0 = Node("S0")

    s1 = Node("S1", s0)

    s2 = Node("S2", s1)
    s3 = Node("S3", s1)
    s4 = Node("S4", s1)

    s5 = Node("S5", s2)
    s6 = Node("S6", s2)

    return s0, [s0, s1, s2, s3, s4, s5, s6]


def setup_():
    s5 = Node("S5")

    s1 = Node("S1", s5)

    s2 = Node("S2", s5)
    s3 = Node("S3", s5)

    return s5, [s1, s2, s3]


def calcSendRecv(node, nNodes, f):
    node.send = {}
    node.recv = {}

    for strength in range(nNodes):
        sumC = 0
        for child in node.children:
            sumC += child.recv[strength]
        node.send[strength] = f(node, strength) + sumC      # Berechnung wenn ich Mast in Node aufstelle
        if strength != nNodes - 1:                          # Berechnung wenn ich Mast in Node.child aufstelle
            for c in node.children:
                tmp = c.send[strength + 1] + (sumC - c.recv[strength])
                if node.send[strength] >= tmp:
                    node.send[strength] = tmp
        node.recv[strength] = 0
        if strength == 0:
            node.recv[strength] = node.send[strength]
        else:
            for child in node.children:
                node.recv[strength] += child.recv[strength - 1]


def fill(root, f, nNodes, cost):
    for n in root.children:
        fill(n, f, nNodes, cost)
    calcSendRecv(root, nNodes, f)
    if root.children is not None:
        for c in root.children:
            if c.children is not None:
                del c.children
    return


def solve(root, nL, f):
    fill(root, f, len(nL), 0)
    return root.send[min(root.send.keys(), key=(lambda k: root.send[k]))]


def f_(node, i):
    return i


if __name__ == '__main__':
    root, nL = setup()
    print_tree(root, horizontal=False)
    print(solve(root, nL, f_))
