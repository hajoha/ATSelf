import timeit
from unittest import TestCase
from ATSelf.aufgabe2_try2 import *
import random
import matplotlib.pyplot as plt


def setup1():
    s0 = Node("S0")
    s1 = Node("S1", s0)
    s2 = Node("S2", s1)
    s3 = Node("S3", s1)

    return s0, [s0, s1, s2, s3]


def setup2():
    s0 = Node("S0")

    s1 = Node("S1", s0)

    s2 = Node("S2", s1)
    s3 = Node("S3", s1)
    s4 = Node("S4", s1)

    s5 = Node("S5", s2)
    s6 = Node("S6", s2)

    return s0, [s0, s1, s2, s3, s4, s5, s6]


def setup3():
    s4 = Node("S4")
    s0 = Node("S0", s4)
    s1 = Node("S1", s4)
    s2 = Node("S2", s4)
    s3 = Node("S3", s4)

    return s4, [s0, s1, s2, s3, s4]


def setup4():
    s0 = Node("S0")
    s1 = Node("S1", s0)
    s2 = Node("S2", s1)
    s3 = Node("S3", s2)

    return s0, [s0, s1, s2, s3]


def generateRandom(n: int):
    s0 = Node("S0")

    nodes = [s0]
    for i in range(1, n):
        nodes.append(Node(str(i), random.choice(nodes)))

    return s0, nodes


def f0(node, i):
    return i


def f1(node, i):
    return i + 1


def f2(node, i):
    return (i + 1) ** 2


def f3(node, i):
    return node.ID + i ** 2


test_cases = [
    (setup1, 2, f1),
    (setup2, 3, f1),
    (setup2, 0, f0),
    (setup2, 6, f2),
    (setup3, 4, f3),
    (setup4, 3, f1),
    (setup4, 4, f2),
    (setup4, 3, f3),
]


class Test(TestCase):
    def test_solve(self):
        for idx, (setup, exp, f) in enumerate(test_cases):
            root, nodeList = setup()
            res = solve(root, nodeList, f)
            if res != exp:
                print_tree(root, horizontal=False)
            print("case: ", idx, "result: ", res, "expected: ", exp)

            self.assertEqual(res, exp, f"Case: {idx}")

    def test_solve_random_ntimes(self):
        maxValue = 50000
        step = 10000
        n = np.arange(step, int(maxValue), step)
        runtime = []
        for i in range(len(n)):
            root, nodeList = generateRandom(n[i])
            start = timeit.default_timer()
            res = solve(root, nodeList, f0)

            stop = timeit.default_timer()
            delta = stop - start

            print(str(n[i]) + "\t", "\t\tdelta: " + str(delta) + "\t\tin sec")
            runtime.append((n[i], delta))

            if res != 0:
                print_tree(root, horizontal=False)

            self.assertEqual(res, 0, f"Rand: {i}")

        plt.scatter(*zip(*runtime))
        plt.plot(*zip(*runtime))
        plt.savefig('plots/' + str(n[-1]) + '.png')
        print(runtime)

        plt.xscale("log")
        plt.scatter(*zip(*runtime))
        plt.plot(*zip(*runtime))
        plt.savefig('plots/' + str(n[-1]) + '_log.png')


if __name__ == '__main__':
    n = Test()
    n.test_solve_random_ntimes()
