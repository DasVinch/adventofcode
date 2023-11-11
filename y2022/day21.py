from enum import Enum
import os
from tools import get_input

from typing import Dict, Union

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'root: pppw + sjmn',
    'pppw: cczh / lfqf',
    'cczh: sllz + lgvd',
    'sllz: 4',
    'lgvd: ljgn * ptdq',
    'ljgn: 2',
    'ptdq: humn - dvpt',
    'humn: 5',
    'dvpt: 3',
    'lfqf: 4',
    'sjmn: drzm * dbpl',
    'drzm: hmdt - zczc',
    'hmdt: 32',
    'zczc: 2',
    'dbpl: 5',
]

REAL = get_input(DAYDAY, 2022)


def doeval(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b

def revevalleft(target: int, op: str, right: int) -> int:
    if op == '+':
        return target - right
    elif op == '-':
        return target + right
    elif op == '*':
        return target / right
    elif op == '/':
        return target * right

def revevalright(target: int, op: str, left: int) -> int:
    if op == '+':
        return target - left
    elif op == '-':
        return left - target
    elif op == '*':
        return target / left
    elif op == '/':
        return left / target


class Leaf:

    def __init__(self, name: str, val: int) -> None:
        self.name: str = name
        self.val: int = val

        self.revval: int = None

    def eval(self) -> int:
        return self.val

    def taghuman(self) -> bool:
        return self.name == "humn"

    def reverseeval(self, target: int) -> None:
        self.revval = target


class LR(Enum):
    L = 0
    R = 1
    NOPE = 2
    LR = 3


class Node:

    def __init__(self, name: str, left: str, right: str, op: str,
                 nodedict: Dict[str, 'Node']) -> None:
        self.name: str = name
        self.op: str = op
        self.leftname: str = left
        self.rightname: str = right

        self.nodedict = nodedict

        self.val: int = None
        self.wherehuman: str = None

    def eval(self) -> int:
        if self.val is not None:
            return self.val
        left = self.nodedict[self.leftname]
        right = self.nodedict[self.rightname]
        self.val = doeval(left.eval(), right.eval(), self.op)

        return self.val

    def reverseeval(self, target: int) -> None:
        if self.wherehuman == LR.L:
            right = self.nodedict[self.rightname]
            val = revevalleft(target, self.op, right.val)
            self.nodedict[self.leftname].reverseeval(val)
        elif self.wherehuman == LR.R:
            left = self.nodedict[self.leftname]
            val = revevalright(target, self.op, left.val)
            self.nodedict[self.rightname].reverseeval(val)
        else:
            raise AssertionError('Wrong wherehuman')
                
    


    def taghuman(self) -> bool:
        if self.wherehuman is not None:
            return self.wherehuman != LR.NOPE

        left = self.nodedict[self.leftname]
        right = self.nodedict[self.rightname]

        lhuman = left.taghuman()
        rhuman = right.taghuman()

        if lhuman and rhuman:
            self.wherehuman = LR.LR
        elif rhuman:
            self.wherehuman = LR.R
        elif lhuman:
            self.wherehuman = LR.L
        else:
            self.wherehuman = LR.NOPE
        return self.wherehuman != LR.NOPE


class Day:

    def __init__(self, lines) -> None:
        self.nodedict: Dict[str, Union[Node, Leaf]] = {}

        for l in lines:
            ass, op = l.split(':')

            ops = op.split()
            if len(ops) == 1:
                self.nodedict[ass] = Leaf(ass, int(op))
            else:
                self.nodedict[ass] = Node(ass, ops[0], ops[2], ops[1],
                                          self.nodedict)

    def solve1(self):
        return self.nodedict['root'].eval()

    def solve2(self):
        root = self.nodedict['root']
        root.taghuman()
        root.eval()

        if root.wherehuman == LR.L:
            target = self.nodedict[root.rightname].val
            scan = self.nodedict[root.leftname]
        elif root.wherehuman == LR.R:
            target = self.nodedict[root.leftname].val
            scan = self.nodedict[root.rightname]
        else:
            raise AssertionError('root.wherehuman wrong')

        scan.reverseeval(target)

        return self.nodedict["humn"].revval


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())