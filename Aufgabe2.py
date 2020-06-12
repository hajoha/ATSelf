from pptree import *
import numpy as np


def setup():
    s1 = Node("S1")

    s2 = Node("S2", s1)

    s3 = Node("S3", s2)
    s4 = Node("S4", s2)
    s5 = Node("S5", s2)

    s6 = Node("S6", s3)
    s7 = Node("S7", s3)

    return s1, [s1, s2, s3, s4, s5, s6, s7]


def sortNodes(nodeList):
    nodeDict = {}
    for node in nodeList:
        nodeDict[node] = len(node.children)
    nodes = sorted(nodeDict.items(), key=lambda x: x[1], reverse=True)

    return nodes


def getNodeID(node):
    return int(node.name[-1])


def hit(node, i):
    if i == 0:
        return [node]
    c = hit_rec(node, i)
    if node.parent is not None:
        c.append(node.parent)
    return c


def hit_rec(node, i):
    if i == 0:
        return [node]
    count = [node]
    for child in node.children:
        count += hit_rec(child, i - 1)
    return count


def calc(prioQ, f, nodeList):
    cost = 0
    for _, nodeID, strength in prioQ:
        if nodeID == strength == -1:
            continue
        nodesHit = hit(nodeList[nodeID], strength)
        for node in nodesHit:
            i = getNodeID(node) - 1
            prioQ[i] = (-1, -1, -1)
        cost += f(nodeList[nodeID], strength)

    return cost


def f_(node, i):
    return i + 1


def solve(nodeList, f):
    nodeListSorted = sortNodes(nodeList)
    Q = []
    for node, child in nodeListSorted:
        nodeID = getNodeID(node) - 1
        max = float("-inf")
        for i in range(len(nodeList)):
            tmp = float("inf")
            if f(node, i) != 0:
                tmp = len(hit(node, i)) / f(node, i + 1)
            if tmp >= max:
                max = tmp
                strength = i

        Q.append((max, nodeID, strength))
        #sorted(Q, key=lambda x: x[1], reverse=True)
    return calc(Q, f, nodeList)


if __name__ == '__main__':
    root, nodeList = setup()
    print_tree(root, horizontal=False)
    print(solve(nodeList, f_))
