import os
import ast
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '',
    '[[1],[2,3,4]]',
    '[[1],4]',
    '',
    '[9]',
    '[[8,7,6]]',
    '',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '',
    '[7,7,7,7]',
    '[7,7,7]',
    '',
    '[]',
    '[3]',
    '',
    '[[[]]]',
    '[[]]',
    '',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]',
]

REAL = get_input(DAYDAY, 2022)


class Day:

    def __init__(self, lines) -> None:
        self.pairs = []
        self.allpackets = [ [[2]], [[6]] ]
        pair = []
        for l in lines:
            if l == '':
                self.pairs += [pair]
                pair = []
            else:
                packet = ast.literal_eval(l)
                pair += [packet]
                self.allpackets += [packet]
        self.pairs += [pair]


    def compare(self, l, r):
        #print(l, r)
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return 1
            elif l == r:
                return 0
            else:
                return -1

        elif isinstance(l, list) and isinstance(r, list):
            if l == [] and r == []:
                return 0
            elif l == [] and len(r) > 0:
                return 1
            elif len(l) > 0 and r == []:
                return -1
            else:
                x = self.compare(l[0], r[0])
                if x != 0:
                    return x
                else:
                    return self.compare(l[1:], r[1:])

        elif isinstance(l, list):
            return self.compare(l, [r])
        else:
            return self.compare([l], r)

    


        
    def solve1(self):
        tot = 0
        for k, p in enumerate(self.pairs):
            if self.compare(*p) == 1:
                tot += k+1

        return tot

    def mergesort(self, l):
        if len(l) <= 1:
            return l

        else:
            n = len(l) // 2
            return self.merge(self.mergesort(l[:n]), self.mergesort(l[n:]))
        
    def merge(self, l1, l2):
        if len(l1) == 0:
            return l2
        elif len(l2) == 0:
            return l1

        if self.compare(l1[0], l2[0]) == 1:
            return [l1[0]] + self.merge(l1[1:], l2)
        else:
            return [l2[0]] + self.merge(l1, l2[1:])


    def solve2(self):
        self.sortedpackets = self.mergesort(self.allpackets.copy())

        return (1+self.sortedpackets.index([[2]])) * (1+self.sortedpackets.index([[6]]))


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    r = Day(REAL)
    print(r.solve1())