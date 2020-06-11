from unittest import TestCase
from ATSelf.Aufgabe2 import *


def setup1():
    s1 = Node("S1")
    s2 = Node("S2", s1)
    s3 = Node("S3", s2)
    s4 = Node("S4", s2)

    return s1, [s1, s2, s3, s4]


def setup2():
    s1 = Node("S1")

    s2 = Node("S2", s1)

    s3 = Node("S3", s2)
    s4 = Node("S4", s2)
    s5 = Node("S5", s2)

    s6 = Node("S6", s3)
    s7 = Node("S7", s3)

    return s1, [s1, s2, s3, s4, s5, s6, s7]


def f0(node, i):
    return i


def f1(node, i):
    return i + 1


def f2(node, i):
    return (i + 1) ** 2


class Test(TestCase):
    def test_solve(self):
        for idx, (setup, exp, f) in enumerate([(setup1, 2, f1), (setup2, 3, f1), (setup2, 0, f0), (setup2, 6, f2)]):
            root, nodeList = setup()
            res = solve(nodeList, f)
            print(idx, res)
            if res != exp:
                print_tree(root, horizontal=False)

            self.assertEqual(res, exp, f"Case: {idx}")
