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


def calcChild(t, ):
    tmp = []
    for c in t:
        for a in c.children:
            tmp.append(a)
        if c.parent is not None:
            tmp.append(c.parent)
    return tmp


def hitNodes(nL, f):
    n = len(nL)
    newDict = {}
    d = {}
    for node in nL:
        cNode = node
        tmp = 0
        for i in range(n):
            if i == 0:
                tmp += f(cNode, i)
                newDict[(cNode, i)] = ([node], f(cNode, i))
            else:
                tmp += f(cNode, i)
                t = node.adj()
                newDict[(cNode, i)] = (set(list(newDict[(cNode, i - 1)][0]) + t), f(cNode, i))
                newNode = Node("mergedNode" + str(i))
                newNode.children = calcChild(t)
                node = newNode
        d[cNode] = tmp
    return newDict, d


def maxValue(eN):
    mN = {}
    for (node, strength), efficiency in eN.items():
        if node in mN:
            if mN[node][0] <= efficiency:
                mN[node] = (efficiency, strength)
        else:
            mN[node] = (efficiency, strength)

    sortmN = sorted(mN.items(), key=lambda x: x[1], reverse=True)
    t = {}
    for node, (efficiency, strength) in sortmN:
        t[node] = (efficiency, strength)
    return t


def sortNodes(nodeList, f, hN):
    nodeDict = {}
    for node in nodeList:
        tmp = []
        for i in range(len(nodeList)):
            tmp += hN[(node, i)]

        nodeDict[node] = f(node, len(tmp) / len(nodeList))
    nodes = sorted(nodeDict.items(), key=lambda x: x[1], reverse=True)

    nodeDict = {}
    for node, adj in nodes:
        nodeDict[node] = adj
    return nodeDict


def clusterNodes(hN, n, f):
    cN = {}
    for (node, strength) in hN.keys():
        if (len(hN[node, strength][0]), strength) in cN:
            cN[(len(hN[node, strength][0]), strength)] = cN[(len(hN[node, strength][0]), strength)] + [node]
        else:
            cN[(len(hN[node, strength][0]), strength)] = [node]

    nodes = sorted(cN.items(), key=lambda x: x[0], reverse=True)
    cN = {}
    for (nHit, strength), node in nodes:
        cN[nHit, strength] = node
    lastNodeClust = {}
    for (hit, strength) in cN.keys():
        # if (n-hit) != 0:
        tmp = (strength, cN[(hit, strength)], f(node, strength))
        if hit in lastNodeClust:
            if lastNodeClust[hit][0] >= strength:
                lastNodeClust[hit] = tmp
        else:
            lastNodeClust[hit] = tmp
    nodes = sorted(lastNodeClust.items(), key=lambda x: x[1][2], reverse=False)
    cN = {}
    i = 0
    for nHit, (strength, node, prob) in nodes:
        prob = 0
        for k in node:
            prob += f(k, strength)
        cN[i] = (nHit, strength, node, prob)
        i += 1
    nodes = sorted(cN.items(), key=lambda x: x[1][3], reverse=False)
    cN = {}
    i = 0
    print(nodes)
    for i, (nHit, strength, node, prob) in nodes:
        cN[i] = (nHit, strength, node, prob)

    return cN


def set_approach(a, b):
    return list(set(a) - set(b))


def cost(cN, hN, f):
    cost = 0
    b = len(cN)
    test = {}
    while len(cN) != 0:
        i = next(iter(cN))
        nHit, strength, node, prob = cN[i]
        test[node[0]] = strength
        for n in node:
            deleteNodes = hN[(n, strength)][0]
            for k in range(b):
                if k in cN:
                    nHit, strength, o, prob = cN[k]
                    goal = set_approach(o, deleteNodes)
                    for g in goal:
                        if g not in test:
                            test[g] = strength
                        else:
                            if test[g] >= strength:
                                test[g] = strength
                    cN[k] = nHit, strength, goal, prob
                    if len(goal) == 0:
                        cN.pop(k)
    for node, strength in test.items():
        cost += f(node, strength)
    return cost


def decideNodes(hN, n, f):
    done = []
    notDone = []
    for key in hN.keys():
        nodes, cost = hN[key]
        if len(nodes) == n:
            tmp = (key, float("-inf"))
            if f(key[0], key[1]) != 0:
                tmp = (key, len(nodes) / f(key[0], key[1]))
            done.append(tmp)
        else:
            tmp = (key, float("-inf"))
            if f(key[0], key[1]) != 0:
                tmp = (key, len(nodes) / f(key[0], key[1]))
            notDone.append(tmp)

    nodesDone = sorted(done, key=lambda x: x[1], reverse=True)
    nodesNotDone = sorted(notDone, key=lambda x: x[1], reverse=True)

    return nodesDone, nodesNotDone


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

    for strength in range(nNodes):
        node.recv[strength] = 0
        if strength == 0:
            node.recv[strength] = node.send[strength]
        else:
            for child in node.children:
                node.recv[strength] += child.recv[strength -1]


def fill(root, f, nNodes, cost):
    for n in root.children:
        fill(n, f, nNodes, cost)
    calcSendRecv(root, nNodes, f)
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
