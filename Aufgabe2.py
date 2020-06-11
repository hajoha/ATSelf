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


def calc(m, nodeList, f):
    max = float("-inf")
    nodeIDx = 0
    strength = 0
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i, j] >= max:
                max = m[i, j]
                nodeIDx = j
                strength = i

    nodesHit = hit(nodeList[nodeIDx], strength)
    for node in nodesHit:
        i = getNodeID(node)
        m[:, i] = 0

    return m, f(nodeList[nodeIDx], strength), nodeList[nodeIDx], strength


def f_(node, i):
    return i+1


def solve(nodeList, f):
    nodeListSorted = sortNodes(nodeList)

    m = np.zeros((len(nodeList), len(nodeList)))
    for node, child in nodeListSorted:
        nodeID = getNodeID(node) - 1
        for i in range(len(nodeList)):
            if f(node, i) == 0:
                m[i, nodeID] = float("inf")
            else:
                m[i, nodeID] = len(hit(node, i)) / f(node, i)

    cost = 0
    emptyList = []
    while 0 != m.any():
        m, tmpcost, node, strength = calc(m, nodeList, f)
        emptyList.append((strength, node.name))
        cost += tmpcost
    print("cost: ", cost)
    return cost

if __name__ == '__main__':
    root, nodeList = setup()
    print_tree(root, horizontal=False)
    nodeListSorted = sortNodes(nodeList)

    m = np.zeros((len(nodeList)+1, len(nodeList)+1))
    for node, child in nodeListSorted:
        nodeID = getNodeID(node)
        for i in range(len(nodeList)):
            m[i, nodeID] = len(hit(node, i)) / f_(node,i)
    print(np.round(m, 2))

    cost = 0
    emptyList = []
    while 0 != m.any():
        m, tmpcost, node, strength = calc(m, nodeList, f_)
        print(np.round(m,2))
        emptyList.append((strength, node.name))
        cost += tmpcost

    print(cost)
    print(emptyList)
