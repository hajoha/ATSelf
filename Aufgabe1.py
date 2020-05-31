import numpy as np


class Tree:
    def __init__(self, ID):
        self.ID = ID
        self.left = None
        self.right = None
        self.val = 0


def setup(arr, root, i, n):
    if i < n:
        temp = Tree(arr[i])
        root = temp
        root.left = setup(arr, root.left, 2 * i + 1, n)
        root.right = setup(arr, root.right, 2 * i + 2, n)
    return root


def calcnodes(k):
    return _calcNodes(2 ** k)


def _calcNodes(k):
    if k == 1:
        return 1
    return k + _calcNodes(int(k / 2))


def traverse(root):
    currentLevel = [root]
    while currentLevel:
        for node in currentLevel:
            print(node.ID, "\t", end='')
        print()
        nextLevel = list()
        for n in currentLevel:
            if n.left:
                nextLevel.append(n.left)
            if n.right:
                nextLevel.append(n.right)
        currentLevel = nextLevel


def calcHight(root):
    if root is None:
        return 0
    return 1 + calcHight(root.left)


def generateNodeList(nLeaf: int):
    nNodes = calcnodes(nLeaf)
    return np.arange(0, nNodes)


def exists(left, right, paths) -> bool:
    if paths[left] == paths[right]:
        return 0
    return 1


def wrapper(root: Tree, relevantNodes):
    nodes = {}
    for i, (l, r) in enumerate(relevantNodes):
        nodes[l] = i
        nodes[r] = i
    return solve(root, nodes)


def solve(root: Tree, tupleMap):
    if root.right is None:
        return [tupleMap[root.ID]], 0
    lList, lVal = solve(root.left, tupleMap)
    rList, rVal = solve(root.right, tupleMap)

    outSet = list(set(lList).symmetric_difference(rList))

    root.val = len(outSet)+root.right.val+root.left.val
    return outSet, root.left.val+root.right.val

if __name__ == '__main__':
    nLeaf = 3

    nodeList = generateNodeList(nLeaf)
    t = setup(nodeList, None, 0, len(nodeList))
    traverse(t)

    relevantNodes = [(7, 14), (8, 9), (10, 13), (11, 12)]  # 10
    #relevantNodes = [(7, 8), (9, 10), (11, 12), (13, 14)]  # 0
    #relevantNodes = [(7, 14), (8, 13), (9, 12), (10, 11)]   # 16
    print(wrapper(t, relevantNodes))

    nLeaf = 2

    nodeList = generateNodeList(nLeaf)
    t = setup(nodeList, None, 0, len(nodeList))
    traverse(t)

    relevantNodes = [(3, 5), (4, 6)]  # 5
    # relevantNodes = [(7, 8), (9, 10), (11, 12), (13, 14)]  # 0
    # relevantNodes = [(7, 14), (8, 13), (9, 12), (10, 11)]   # 16
    print(wrapper(t, relevantNodes))
