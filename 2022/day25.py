import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '1=-0-2',
    '12111',
    '2=0=',
    '21',
    '2=01',
    '111',
    '20012',
    '112',
    '1=-1=',
    '1-12',
    '12',
    '1=',
    '122',
]

REAL = get_input(DAYDAY, 2022)

MAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}
REVMAP = ['0', '1', '2', '=', '-']


class Day:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.decimal = []

    def solve(self):
        for l in self.lines:
            n = 0
            for c in l:
                n *= 5
                n += MAP[c]
            self.decimal += [n]

        total = sum(self.decimal)
        print(total)

        if total == 0:
            return '0'
        s = ''
        while total > 0:
            x = (total + 2) % 5 - 2
            s = REVMAP[x] + s
            total -= x
            total //= 5

        return s


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve())
    r = Day(REAL)
    print(r.solve())