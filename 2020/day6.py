import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'abc',
    '',
    'a',
    'b',
    'c',
    '',
    'ab',
    'ac',
    '',
    'a',
    'a',
    'a',
    'a',
    '',
    'b',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.grouped = []
        grp = []
        for line in lines + ['']:
            if line == '':
                self.grouped += [grp]
                grp = []
            else:
                grp += [line]

    def solve1(self):
        self.gsets = []
        tot = 0
        for g in self.grouped:
            gset = set()
            for l in g:
                for c in l:
                    gset.add(c)
            self.gsets += [gset]

            tot += len(gset)

        return tot

    def solve2(self):
        self.gsets = []
        tot = 0
        for g in self.grouped:
            gset = {}
            for l in g:
                for c in l:
                    gset[c] = gset.get(c, 0) + 1
            self.gsets += [gset]

            tot += len([gset[k] for k in gset if gset[k] == len(g)])

        return tot

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())