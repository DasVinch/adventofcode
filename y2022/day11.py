import os
from tools import get_input
from enum import Enum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

class Op(Enum):
    MUL = 0
    ADD = 1
    SUB = 2
    DIV = 3

class Monkey:
    def __init__(self, items, op, testmod, true, false) -> None:
        self.items = items
        self.op = op[0]
        self.op2 = op[1]
        self.testmod = testmod
        self.true = true
        self.false = false

        self.howmany = 0

    def oper(self, old):
        if self.op2 != 'o':
            if self.op == Op.ADD:
                return old + self.op2
            elif self.op == Op.MUL:
                return old * self.op2
        else:
            if self.op == Op.ADD:
                return old + old
            elif self.op == Op.MUL:
                return old * old

    def registerMonkeys(self, monkeys):
        self.allmonkeys = monkeys

    def round(self, cm=None, no_3: bool = False):
        n = len(self.items)
        for k in range(n):
            item = self.items.pop(0)
            if cm is None:
                new = self.oper(item)
            else:
                new = self.oper(item) % cm
            if not no_3:
                new //= 3
            if new % self.testmod == 0:
                self.allmonkeys[self.true].items.append(new)
            else:
                self.allmonkeys[self.false].items.append(new)
            self.howmany += 1

def mksample():
    return [
        Monkey([79, 98], (Op.MUL, 19), 23, 2, 3),
        Monkey([54,65,75,74], (Op.ADD, 6), 19, 2, 0),
        Monkey([79,60,97], (Op.MUL, 'o'), 13, 1, 3),
        Monkey([74], (Op.ADD, 3), 17, 0, 1),
    ]

def mkreal():
    return [
        Monkey([91, 58, 52, 69, 95, 54], (Op.MUL, 13), 7, 1, 5),
        Monkey([80, 80, 97, 84], (Op.MUL, 'o'), 3, 3, 5),
        Monkey([86, 92, 71], (Op.ADD, 7), 2, 0, 4),
        Monkey([96, 90, 99, 76, 79, 85, 98, 61], (Op.ADD, 4), 11, 7, 6),
        Monkey([60, 83, 68, 64, 73], (Op.MUL, 19), 17, 1, 0),
        Monkey([96, 52, 52, 94, 76, 51, 57], (Op.ADD, 3), 5, 7, 3),
        Monkey([75], (Op.ADD, 5), 13, 4, 2),
        Monkey([83, 75], (Op.ADD, 1), 19, 2, 6),
    ]

class Day:
    def __init__(self, raw_monkeys) -> None:
        self.monkeys = raw_monkeys
        for m in self.monkeys:
            m.registerMonkeys(self.monkeys)

    def round(self, cm = None, no_3 = False):
        for m in self.monkeys:
            m.round(cm, no_3)

    def mbus(self):
        activity = [m.howmany for m in self.monkeys]
        activity.sort(reverse=True)
        return activity[0] * activity[1]


    def solve1(self):
        for i in range(20):
            self.round()
        return self.mbus()

    def solve2(self):
        prod = 1
        for mm in [m.testmod for m in self.monkeys]:
            prod *= mm
        for i in range(10000):
            self.round(prod, no_3=True)
        return self.mbus()
        

if __name__ == "__main__":
    t = Day(mksample())
    print(t.solve1())
    t = Day(mksample())
    print(t.solve2())
    r = Day(mkreal())
    print(r.solve1())
    r = Day(mkreal())
    print(r.solve2())